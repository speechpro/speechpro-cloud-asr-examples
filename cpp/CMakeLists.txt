cmake_minimum_required (VERSION 3.1.0)

project(cppExample)

if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(WINDOWS 1)
    message (STATUS "Operating system is: Windows")
    add_definitions(-DWIN32)
	add_definitions(-D_WIN32_WINNT=0x0601)
endif()

set_property(GLOBAL PROPERTY USE_FOLDERS TRUE)
define_property(
    TARGET
    PROPERTY FOLDER
    INHERITED
    BRIEF_DOCS "Set the folder name."
    FULL_DOCS  "Use to organize targets in an IDE."
)

function(add_subdirectory_with_folder _folder_name _folder)
    add_subdirectory(${_folder} ${ARGN})
    set_property(DIRECTORY "${_folder}" PROPERTY FOLDER "${_folder_name}")
endfunction()

message(STATUS "CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH}")

set(CMAKE_DEBUG_POSTFIX "D")
set(CMAKE_MINSIZEREL_POSTFIX "S")
set(CMAKE_RELWITHDEBINFO_POSTFIX "RD")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory_with_folder("gRPC" third_party/grpc)

add_subdirectory(proto)
add_subdirectory(GRPCExample)

add_custom_command(
	OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/roots.pem
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_SOURCE_DIR}/GRPCPem/roots.pem
    ${CMAKE_CURRENT_BINARY_DIR})

