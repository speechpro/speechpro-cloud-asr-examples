#include <iostream>
#include <string>
#include <memory>
#include <future>

#include <proto/AsrService.grpc.pb.h>
#include <grpc++/channel.h>

class IResult {
public:
	virtual void ReceiveResult(Speechpro::Cloud::ASR::SpeechRecognitionResults result) = 0;
};

class SpeechRecognizerSevice {
public:
	SpeechRecognizerSevice(std::shared_ptr<grpc::Channel> _channel, std::shared_ptr<IResult> _callback);

	void RecognizeConfig(const std::string& _modelID, const Speechpro::Cloud::ASR::Auth& _authData);
	void Recognize(Speechpro::Cloud::ASR::RecognizeRequest& request);
	void FinishRecognition();

private:
	void configureStream();
	void recognitionResult();


	template<typename T, typename D>
	struct BidirectionalStream {
		std::shared_ptr< ::grpc::ClientReaderWriter< T, D>> stream;		
		grpc::ClientContext context;
	};

	std::future<void> m_resultAsync;
	std::unique_ptr<BidirectionalStream<Speechpro::Cloud::ASR::RecognizeRequest, Speechpro::Cloud::ASR::SpeechRecognitionResults>> m_stream;
	std::shared_ptr<Speechpro::Cloud::ASR::SpeechRecognition::Stub> m_stub;
	std::shared_ptr<IResult> m_callBackResult;
protected:

};


