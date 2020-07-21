const fs = require('fs');
const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const wav = require('wav');

const client_id = process.env.SPEECHPRO_USERNAME;
const domain_id = process.env.SPEECHPRO_DOMAIN_ID;
const api_key = process.env.SPEECHPRO_PASSWORD;

var file = fs.createReadStream(process.argv[2]);
var reader = new wav.Reader();

const request = {
    config: {
        model: { id: 'general' },
        auth: {
            clientId: client_id,
            domainId: domain_id,
            apiKey: api_key
        }
    }
};

const CHUNK_SIZE = 8000;
const DELAY = CHUNK_SIZE * 1000 / ( 2 * 16000);

const packageDefinition = protoLoader.loadSync('./proto/AsrService.proto', {
    includeDirs: ['node_modules/google-proto-files', './proto']
});
const packageObject = grpc.loadPackageDefinition(packageDefinition);

// Установить соединение с сервером.
const serviceConstructor = packageObject.Speechpro.Cloud.ASR.SpeechRecognition;
const grpcCredentials = grpc.credentials.createSsl(fs.readFileSync('./roots.pem'));
const service = new serviceConstructor('asr.cp.speechpro.com', grpcCredentials);
const call = service['RecognizeSpeech']();

// Отправить сообщение с настройками распознавания.
call.write(request);

reader.on('readable', function () {
    const interval = setInterval(() => {
        samples = reader.read(CHUNK_SIZE);
        if (samples) {
            call.write({ sound: { samples: samples }});
        } else {
            clearInterval(interval);
        }
    }, DELAY);
});
reader.on("end", function () {
    call.write({ finish: {} });
    call.end();
});

file.pipe(reader);

call.on('data', (response) => {
    const sentence = response.text.words.map(w => w.text).join(' ');
    console.log(`${ response.isFinal ? '\x1b[32m' : '\x1b[2m'}${sentence}\x1b[0m`);
});

call.on('error', (response) => {
    console.log(response);
});