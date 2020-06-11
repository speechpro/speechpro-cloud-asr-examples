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

find_package(protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)

add_subdirectory(proto)
add_subdirectory(GRPCExample)

