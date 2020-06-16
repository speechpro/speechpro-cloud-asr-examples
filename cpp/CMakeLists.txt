cmake_minimum_required (VERSION 3.1.0)

project(cppExample)

if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(WINDOWS 1)
    message (STATUS "Operating system is: Windows")
    add_definitions(-DWIN32)
	add_definitions(-D_WIN32_WINNT=0x0601)
endif()

message(STATUS "CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH}")

set(CMAKE_DEBUG_POSTFIX "D")
set(CMAKE_MINSIZEREL_POSTFIX "S")
set(CMAKE_RELWITHDEBINFO_POSTFIX "RD")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(third_party/grpc)

FILE(GLOB_RECURSE third_party "third_party/*")
SOURCE_GROUP("third_party" FILES ${third_party})

add_subdirectory(proto)
add_subdirectory(GRPCExample)

add_custom_command(
	OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/roots.pem
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_SOURCE_DIR}/GRPCPem/roots.pem
    ${CMAKE_CURRENT_BINARY_DIR})

