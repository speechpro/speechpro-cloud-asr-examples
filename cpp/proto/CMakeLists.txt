set(PROTOBUF_FILES 
    ${CMAKE_CURRENT_SOURCE_DIR}/AsrService.proto
    ${CMAKE_CURRENT_SOURCE_DIR}/base.proto
)

get_target_property(gRPC_CPP_PLUGIN_EXECUTABLE gRPC::grpc_cpp_plugin
		IMPORTED_LOCATION_RELEASE)

protobuf_generate_cpp(hw_microkernel_core_service_proto_srcs hw_microkernel_core_service_proto_hdrs "${PROTOBUF_FILES}")

set(hw_grpc_core_srcs "${CMAKE_BINARY_DIR}/proto/AsrService.grpc.pb.cc")
set(hw_grpc_core_hdrs "${CMAKE_BINARY_DIR}/proto/AsrService.grpc.pb.h")

if(TARGET protobuf::protoc)
    set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)
else()
    set(_PROTOBUF_PROTOC ${PROTOBUF_PROTOC_EXECUTABLE})
endif()

add_custom_command(
    OUTPUT "${hw_grpc_core_srcs}" "${hw_grpc_core_hdrs}"
    COMMAND ${_PROTOBUF_PROTOC}
    ARGS --grpc_out "${CMAKE_BINARY_DIR}/proto" -I "${CMAKE_CURRENT_SOURCE_DIR}"
      --plugin=protoc-gen-grpc="${gRPC_CPP_PLUGIN_EXECUTABLE}"
      "${CMAKE_CURRENT_SOURCE_DIR}/AsrService.proto"
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/AsrService.proto")

add_library(ProtobufGenerated STATIC 
    ${hw_microkernel_core_service_proto_srcs}
    ${hw_microkernel_core_service_proto_hdrs}
    ${hw_grpc_core_srcs}
    ${hw_grpc_core_hdrs}
    )

target_include_directories(ProtobufGenerated
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}>)

target_link_libraries(ProtobufGenerated
    gRPC::gpr)
