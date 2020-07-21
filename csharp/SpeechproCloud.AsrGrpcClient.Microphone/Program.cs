using System;
using System.Threading;
using System.Threading.Tasks;
using System.Linq;

using Grpc.Net.Client;
using Grpc.Core;
using NAudio.Wave;

using Speechpro.Cloud.ASR;

namespace SpeechproCloud.AsrGrpcClient.Microphone
{
    class Program
    {
        private static async Task RecognizeRequest(
            SpeechRecognition.SpeechRecognitionClient client, string model, string client_id, string domain_id, string api_key)
        {
            using var call = client.RecognizeSpeech();

            var responseTask = Task.Run(async () => {
                await foreach(var result in call.ResponseStream.ReadAllAsync()) {
                    var words = from w in result.Text.Words select w.Text;
                    Console.ForegroundColor = result.IsFinal ? ConsoleColor.DarkGreen : ConsoleColor.Gray;
                    Console.WriteLine(string.Join(" ", words));
                    Console.ResetColor();
                }
            });

            var recorder = new WaveInEvent();
            recorder.WaveFormat = new WaveFormat(16000, 1);
            recorder.BufferMilliseconds = 200;

            try
            {

                var config = new RecognizeRequest
                {
                    Config = new RecognitionConfig
                    {
                        Model = new Model { Id = model },
                        Auth = new Auth { ClientId = client_id, DomainId = domain_id, ApiKey = api_key }
                    }
                };
                await call.RequestStream.WriteAsync(config);

                recorder.DataAvailable += async (object sender, WaveInEventArgs e) =>
                {
                    await call.RequestStream.WriteAsync(new RecognizeRequest
                    {
                        Sound = new Sound { Samples = Google.Protobuf.ByteString.CopyFrom(e.Buffer) }
                    });
                };
                recorder.StartRecording();
                Console.WriteLine("Started  recording. Press ESC to stop...");

                while(!(Console.KeyAvailable && Console.ReadKey(true).Key == ConsoleKey.Escape)) {
                    Thread.Sleep(100);
                }

            }
            catch (Exception)
            {
                throw;
            }
            finally
            {
                Console.WriteLine("Stopping recording...");
                recorder.StopRecording();
                await call.RequestStream.WriteAsync(new RecognizeRequest { Finish = new Finish() });
            }

            await call.RequestStream.CompleteAsync();
            await responseTask;
            }

        static async Task Main(string[] args)
        {
            string model = args[0], client_id = args[1], domain_id = args[2], api_key = args[3];
            using var channel = GrpcChannel.ForAddress("https://asr.cp.speechpro.com");
            var client = new SpeechRecognition.SpeechRecognitionClient(channel);
            await RecognizeRequest(client, model, client_id, domain_id, api_key);
        }
    }
}