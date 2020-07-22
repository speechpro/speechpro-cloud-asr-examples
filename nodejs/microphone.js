const fs = require('fs');
var mic = require('mic');
const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');


const packageDefinition = protoLoader.loadSync('proto/AsrService.proto', {
    includeDirs: ['node_modules/google-proto-files', 'proto']
});
const packageObject = grpc.loadPackageDefinition(packageDefinition);

const serviceConstructor = packageObject.Speechpro.Cloud.ASR.SpeechRecognition;
const grpcCredentials = grpc.credentials.createSsl(fs.readFileSync('./roots.pem'));
const service = new serviceConstructor('asr.cp.speechpro.com', grpcCredentials);
const call = service['RecognizeSpeech']();

const config = {
    config: {
        model: { id: 'general' },
        auth: {
            clientId: process.env.SPEECHPRO_USERNAME,
            domainId: process.env.SPEECHPRO_DOMAIN_ID,
            apiKey: process.env.SPEECHPRO_PASSWORD
        }
    }
};
call.write(config);

var micInstance = mic({
    rate: '16000',
    channels: '1'
});
var micInputStream = micInstance.getAudioStream();

var finishSent = false;

// Отправляем сообщения со звуком
micInputStream.on('data', function (data) {
    if(!finishSent) {
        call.write({ sound: { samples: data }});
    }
});
micInputStream.on('stopComplete', function() {
    call.write({ finish: {} });
    call.end();
    finishSent = true;
});


// Обработка результатов
call.on('data', (response) => {
    const sentence = response.text.words.map(w => w.text).join(' ');
    console.log(`${ response.isFinal ? '\x1b[32m' : '\x1b[2m'}${sentence}\x1b[0m`);
});

call.on('end', function() {
    process.exit(0);
});

call.on('error', (response) => {
    console.log(`Error: ${response}`);
});


// Остановить запись звука с микрофона и распознавание речи
console.log('Press any key to exit...');
process.stdin.setRawMode(true);
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', function( key )
{
    micInstance.stop();
});

micInstance.start();