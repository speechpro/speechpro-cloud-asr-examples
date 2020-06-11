#include "SpeechRecognizerService.h"
#include <sstream>


SpeechRecognizerSevice::SpeechRecognizerSevice(std::shared_ptr<grpc::Channel> _channel, std::shared_ptr<IResult> _callback)
	: m_stub(Speechpro::Cloud::ASR::SpeechRecognition::NewStub(_channel))
	, m_callBackResult(_callback)
{
	;
}


void SpeechRecognizerSevice::RecognizeConfig(const std::string& _modelID, const Speechpro::Cloud::ASR::Auth& _authData)
{
	if (!m_callBackResult) {
		throw std::runtime_error("Callback do not set");
	}

	try {
		Speechpro::Cloud::ASR::ListOfModels listOfSpeechRecognitionModels;
		grpc::ClientContext context;
		const auto status = m_stub->GetListOfSpeechRecognitionModels(&context, _authData, &listOfSpeechRecognitionModels);

		if (!status.ok()) {
			std::stringstream stringstream;
			stringstream << "Exception in gRPC: " << status.error_message();
			const auto errorString = stringstream.str();
			throw std::runtime_error(errorString.c_str());
		}

		bool modelFound = false;

		for (const auto& serviceModel : listOfSpeechRecognitionModels.models()) {
			if (serviceModel.id() == _modelID) {
				modelFound = true;
				break;
			}
		}

		if (!modelFound) {
			std::cerr << "Model not found" << std::endl;
			std::cerr << "Available models:" << std::endl;
			for (const auto& serviceModel : listOfSpeechRecognitionModels.models()) {
				std::cerr << "model " << serviceModel.id() << std::endl;
			}
			throw std::runtime_error("Model not found");
		}

		configureStream();

		// начинаем слушать ответы от сервиса
		m_resultAsync = std::async(&SpeechRecognizerSevice::recognitionResult, this);

		Speechpro::Cloud::ASR::RecognizeRequest request;
		auto reqModel = request.mutable_config()->mutable_model();
		reqModel->set_id(_modelID);
		request.mutable_config()->mutable_auth()->CopyFrom(_authData);

		if (!m_stream->stream->Write(request)) {
			auto status = m_stream->stream->Finish();
			if (!status.ok()) {
				throw std::runtime_error(status.error_message());
			}
			std::cerr << "Stream closed" << std::endl;
			throw std::runtime_error("Stream closed");
		}
	}
	catch (const std::exception& ex)
	{
		std::cerr << "ERROR: " << ex.what() << std::endl;;
	}
	catch (...)
	{
		std::cerr << "Internal Error" << std::endl;
	}
}


void SpeechRecognizerSevice::Recognize(Speechpro::Cloud::ASR::RecognizeRequest& request)
{
	if (!m_stream) {
		throw std::runtime_error("Stream do not configured");
	}

	if (!m_stream->stream->Write(request)) {
		auto status = m_stream->stream->Finish();
		if (!status.ok()) {
			throw std::runtime_error(status.error_message());
		}
		std::cerr << "Stream closed" << std::endl;
		throw std::runtime_error("Stream closed");
	}
}


void SpeechRecognizerSevice::FinishRecognition()
{
	if (!m_stream) {
		throw std::runtime_error("Stream do not configured");
	}

	Speechpro::Cloud::ASR::RecognizeRequest request;
	Speechpro::Cloud::ASR::Finish recogFinish;
	request.mutable_finish();

	if (!m_stream->stream->Write(request)) {
		std::cerr << "Stream closed" << std::endl;
		throw std::runtime_error("Stream closed");
	}

	m_stream->stream->WritesDone();
	auto status = m_stream->stream->Finish();
	if (!status.ok()) {
		throw std::runtime_error(status.error_message());
	}

	// дожидаемся когда придет последний результат от сервиса
	if (m_resultAsync.valid())
		m_resultAsync.get();
}


void SpeechRecognizerSevice::configureStream()
{
	m_stream.reset(new BidirectionalStream<Speechpro::Cloud::ASR::RecognizeRequest, Speechpro::Cloud::ASR::SpeechRecognitionResults>);
	m_stream->stream = m_stub->RecognizeSpeech(&m_stream->context);
}

void SpeechRecognizerSevice::recognitionResult()
{
	Speechpro::Cloud::ASR::SpeechRecognitionResults msg;
	while (m_stream->stream->Read(&msg)) {
		m_callBackResult->ReceiveResult(msg);
	}
}

