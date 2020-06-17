set(GRPCEXAMPLE_SOURCE
    src/main.cpp
    src/SpeechRecognizerService.cpp
    )

set(GRPCEXAMPLE_INCLUDE 
    include/SpeechRecognizerService.h    
    include/WAVReader.h
    )

add_executable(GRPCExample 
    ${GRPCEXAMPLE_SOURCE}
    ${GRPCEXAMPLE_INCLUDE}
    )

message(STATUS "CMAKE_CURRENT_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}")

target_include_directories(GRPCExample
    PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)

target_link_libraries(GRPCExample
    libprotobuf
    ProtobufGenerated
    grpc++
    grpc
    gpr
    )

add_custom_command(
    TARGET GRPCExample POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_SOURCE_DIR}/../GRPCPem/roots.pem
    $<TARGET_FILE_DIR:GRPCExample>)

if(WIN32)
add_custom_command(
    TARGET GRPCExample POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_SOURCE_DIR}/../GRPCPem/roots.pem
    $<TARGET_FILE_DIR:GRPCExample>/../)
endif()

install(TARGETS GRPCExample DESTINATION bin)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../GRPCPem/roots.pem DESTINATION bin)
