#pragma once
#include <string>
#include <cstdint>
#include <fstream>
#include <stdexcept>
#include <sstream>

typedef struct {
	uint8_t RIFF[4];
	uint32_t ChunkSIze;
	uint8_t WAVE[4];
	uint8_t fmt[4];
	uint32_t SubchunkSize;
	uint16_t AudioFormat;
	uint16_t NumOfChan;
	uint32_t SamplesPerSec;
	uint32_t bytesPerSec;
	uint16_t blockAlign;
	uint16_t bitsPerSample;
	uint8_t Subchunk2ID[4];
	uint32_t Subchunk2Size; 
} WAV_HEADER;


class WavReader {
public:
	WavReader() = default;

	~WavReader() {
		if (m_wavFile.is_open()) {
			m_wavFile.close();
		}
	}

	void open(const std::string& _filePath) {
		m_wavFile.open(_filePath, std::ios::binary);

		if (m_wavFile.is_open()) {
			m_wavFile.read((char*)&m_wavHeader, sizeof(WAV_HEADER));

			if (m_wavHeader.blockAlign != 2)
			{
				throw std::runtime_error("Unsupported block align!");
			}

			if (m_wavHeader.AudioFormat != 1) {
				throw std::runtime_error("Unsupported audio format!");
			}

		}
		else {
			std::stringstream ss;
			ss << "File " << _filePath << " not found!";
			const auto errorString = ss.str();
			throw std::runtime_error(errorString.c_str());
		}
	}


	uint64_t Read(std::vector<int16_t>& soundSamples, uint32_t sampleCount = 4000) {
		uint64_t readedSamples = 0;
		soundSamples.clear();
		soundSamples.resize(sampleCount);
		soundSamples.reserve(sampleCount);

		readedSamples = m_wavFile.read((char*)&soundSamples[0], (m_wavHeader.bitsPerSample / 8) * sampleCount).gcount();
		soundSamples.resize(readedSamples / (m_wavHeader.bitsPerSample / 8));

		return readedSamples;
	}

private:
	std::ifstream m_wavFile;
	WAV_HEADER m_wavHeader;
};

