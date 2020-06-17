#include <iostream>
#include <fstream>
#include <grpc++/create_channel.h>
#include <ares.h>

#include "SpeechRecognizerService.h"
#include "WAVReader.h"

#ifdef _WINDOWS
#include <windows.h>
#endif

class ResultCallback : public IResult
{
public:
	virtual void ReceiveResult(Speechpro::Cloud::ASR::SpeechRecognitionResults results) override
	{
		if (results.is_final()) {
			for (size_t i = 0; i < results.text().words_size(); ++i) {
				std::cout << results.text().words(i).text() << " ";
			}
			std::cout << std::endl;
		}
	}

private:
};

int main(int argc, char** argv)
{
#ifdef _WINDOWS
	SetConsoleOutputCP(65001);
#else
	setlocale(LC_ALL, "");
#endif	

	if (argc != 7) {
		std::cout << "Usage GRPCExample <server address> <modelName> <client_id> <domain_id> <api_key> <path_to_wav_file>" << std::endl;
		return -1;
	}

	std::string serverAddress(argv[1]);
	std::string modelName(argv[2]);
	std::string clientID(argv[3]);
	std::string domainID(argv[4]);
	std::string apiKey(argv[5]);
	std::string pathToWavFile(argv[6]);

	std::cout << "Server address: " << serverAddress
		<< "\nrequested model: " << modelName
		<< "\nPath to wav file: " << pathToWavFile
		<< std::endl;

	grpc::SslCredentialsOptions credOpt;

	std::ifstream rootsPem("roots.pem", std::ios::in);
	std::string rootCerts((std::istreambuf_iterator<char>(rootsPem)),
		std::istreambuf_iterator<char>());
	rootsPem.close();

	credOpt.pem_root_certs = rootCerts;
	auto channelCreds = grpc::SslCredentials(credOpt);

	// Создаем grpc::Channel один раз на все последующие сессии распознавания, так как создание grpc::Channel 
	std::shared_ptr<grpc::Channel> channel = grpc::CreateChannel(serverAddress, channelCreds);

	WavReader wavReader;
	wavReader.open(pathToWavFile);

	auto callback = std::make_shared<ResultCallback>();
	SpeechRecognizerSevice service(channel, callback);

	Speechpro::Cloud::ASR::Auth authData;
	authData.set_api_key(apiKey);
	authData.set_client_id(clientID);
	authData.set_domain_id(domainID);

	// Конфигурируем сессию распознавания с определенной моделью
	service.RecognizeConfig(modelName, authData);

	std::vector<int16_t> soundSamples;
	int readed = 0;
	while (readed = wavReader.Read(soundSamples))
	{
		Speechpro::Cloud::ASR::RecognizeRequest request;
		request.mutable_sound()->set_samples((const char*)&soundSamples[0], readed);
		service.Recognize(request);
	}

	// Отправляем финальный запрос и дожидаемся всех сообщений от сервиса
	service.FinishRecognition();

	return 0;
}

