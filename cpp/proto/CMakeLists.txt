set(PROTOBUF_FILES 
    ${CMAKE_CURRENT_SOURCE_DIR}/AsrService.proto
    ${CMAKE_CURRENT_SOURCE_DIR}/base.proto
)

set(gRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:grpc_cpp_plugin>)
set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)

set(hw_grpc_core_srcs "${CMAKE_BINARY_DIR}/proto/AsrService.grpc.pb.cc")
set(hw_grpc_core_hdrs "${CMAKE_BINARY_DIR}/proto/AsrService.grpc.pb.h")
set(hw_base_srcs "${CMAKE_BINARY_DIR}/proto/base.pb.cc")
set(hw_base_hdrs "${CMAKE_BINARY_DIR}/proto/base.pb.h")
set(hw_core_service_proto_hdrs "${CMAKE_BINARY_DIR}/proto/AsrService.pb.cc")
set(hw_core_service_proto_srcs "${CMAKE_BINARY_DIR}/proto/AsrService.pb.h")

if(TARGET protobuf::protoc)
    set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)
else()
    set(_PROTOBUF_PROTOC ${PROTOBUF_PROTOC_EXECUTABLE})
endif()

add_custom_command(
    OUTPUT "${hw_base_srcs}" "${hw_base_hdrs}" "${hw_core_service_proto_srcs}" "${hw_core_service_proto_hdrs}" "${hw_grpc_core_srcs}" "${hw_grpc_core_hdrs}"
    COMMAND ${_PROTOBUF_PROTOC}
    ARGS
        --grpc_out "${CMAKE_BINARY_DIR}/proto"
        --cpp_out "${CMAKE_BINARY_DIR}/proto"
        -I "${CMAKE_CURRENT_SOURCE_DIR}"
        --plugin=protoc-gen-grpc="${gRPC_CPP_PLUGIN_EXECUTABLE}"
        ${PROTOBUF_FILES}
    DEPENDS ${PROTOBUF_FILES})

add_library(ProtobufGenerated STATIC 
    ${hw_core_service_proto_srcs}
    ${hw_core_service_proto_hdrs}
    ${hw_base_srcs}
    ${hw_base_hdrs}
    ${hw_grpc_core_srcs}
    ${hw_grpc_core_hdrs}
    )

target_include_directories(ProtobufGenerated
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}>)

target_link_libraries(ProtobufGenerated
    libprotobuf
    gpr)
