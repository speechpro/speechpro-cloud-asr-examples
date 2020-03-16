using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using System.Linq;

using Grpc.Net.Client;
using Grpc.Core;
using NAudio.Wave;

using Speechpro.Cloud.ASR;

namespace SpeechProAsrGrpcClient
{
    class Program
    {
        private static async IAsyncEnumerable<RecognizeRequest> GenerateRequestStream(string filename, string model)
        {
            yield return new RecognizeRequest {
                Config = new RecognitionConfig {
                    Model = new Model { Id = model },
                    Auth = new Auth {
                        ClientId = "ClientId",
                        DomainId = "DomainId",
                        ApiKey = "ApiKey"
                    }
                }
            };

            using var reader = new WaveFileReader(filename);
            int bytesPerSecond = reader.WaveFormat.AverageBytesPerSecond;
            var buffer = new byte[bytesPerSecond];
            while (reader.Position < reader.Length) {
                int bytesRead = await reader.ReadAsync(buffer, 0, bytesPerSecond);
                if (bytesRead > 0) {
                    yield return new RecognizeRequest { 
                        Sound = new Sound { Samples = Google.Protobuf.ByteString.CopyFrom(buffer) }
                    };
                    Thread.Sleep(1000);
                }
            }

            yield return new RecognizeRequest { Finish = new Finish() };
        }

        private static async Task RecognizeRequest(
            SpeechRecognition.SpeechRecognitionClient client, string filename, string model)
        {
            using var call = client.RecognizeSpeech();

            var responseTask = Task.Run(async () => {
                await foreach(var result in call.ResponseStream.ReadAllAsync()) {
                    var words = from w in result.Text.Words select w.Text;
                    Console.ForegroundColor = result.IsFinal ? ConsoleColor.DarkGreen : ConsoleColor.Gray;
                    Console.WriteLine(String.Join(" ", words));
                    Console.ResetColor();
                }
            });

            await foreach(var request in GenerateRequestStream(filename, model)) {
                await call.RequestStream.WriteAsync(request);
            }

            await call.RequestStream.CompleteAsync();
            await responseTask;
        }
        
        static async Task Main(string[] args)
        {
            string filename = args[0], model = args[1];
            using var channel = GrpcChannel.ForAddress("https://asr.cp.speechpro.com");
            var client = new SpeechRecognition.SpeechRecognitionClient(channel);
            await RecognizeRequest(client, filename, model);
        }
    }
}
