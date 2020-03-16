pushd %~dp0
:: Install requirements
REM python -m pip install --proxy proxy2.stc:3128 -r "requirements.txt"
python -m pip install -r "requirements.txt"

:: Generate python code from proto files
python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/base.proto
python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/MicroKernelService.proto
python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/TextTransformService.proto

popd

pause