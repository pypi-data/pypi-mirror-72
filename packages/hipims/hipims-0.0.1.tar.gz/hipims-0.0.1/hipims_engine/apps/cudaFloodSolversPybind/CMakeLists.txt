cmake_minimum_required(VERSION 3.11)

set(EXE flood)
set(SRCS cuda_flood_solvers_pybind.cu)

#set (CUDA_NVCC_FLAGS "-arch=sm_20 -Xptxas=v")
#set (CUDA_SEPARABLE_COMPILATION ON)

file(GLOB_RECURSE gc_headers "${PROJECT_SOURCE_DIR}/hipims_engine/lib/include/*.h")

set (GC_INCLUDE_DIRS "")
foreach (_header_file ${gc_headers})
	get_filename_component(_dir ${_header_file} DIRECTORY)
	list (APPEND GC_INCLUDE_DIRS ${_dir})
endforeach()
list(REMOVE_DUPLICATES GC_INCLUDE_DIRS)

include_directories(${GC_INCLUDE_DIRS})
include_directories("${pybind11_sources_SOURCE_DIR}/include")
include_directories(${PYTHON_INCLUDE_DIRS})

cuda_add_library(${EXE} MODULE ${SRCS})
add_dependencies(${EXE} lib cuda_lib)

#set (CUDA_NVCC_FLAGS "-arch=sm_35")

target_link_libraries(${EXE} lib cuda_lib)
target_link_libraries(${EXE} pybind11::module)

set_target_properties(${EXE} PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
                                        SUFFIX "${PYTHON_MODULE_EXTENSION}")
#set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/release/bin)
#set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/release/lib)

install(
  TARGETS
    ${flood}
  LIBRARY
    DESTINATION ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/hipims_engine
  )
