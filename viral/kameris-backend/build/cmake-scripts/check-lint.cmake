set(PROJECT_SOURCES "/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/benchmarks/benchmark.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/representations.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances-sparse/utils.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances-sparse/euclidean_manhattan.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances-sparse/cosine_pearson.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances-sparse/information.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils/parallel.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils/types.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils/random.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils/time.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils/matrix_vector_adapters.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils/math.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/utils/fasta.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances/utils.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances/euclidean_manhattan.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances/cosine_pearson.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances/ssim.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances/information.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/representations/cgr.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/representations/twocgr.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/representations/descriptor.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/libkameris/distances-sparse.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/all_formats.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/dist_writer.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/element_type.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/repr_writer.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/common/pseudo_cast.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/common/binary_io.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/common/storage_encoding.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/common/binary_collection_io.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/repr_reader.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/dist_reader.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/kameris-formats/cpp/headers.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/src/common/progress_bar.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/src/common/version.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/src/common/progress_bar.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/src/generation_cgr.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/src/generation_dists.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/libkameris/fasta.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/libkameris/random.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/libkameris/distances-sparse.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/libkameris/parallel.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/libkameris/distances.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/libkameris/representations.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/test_helpers.hpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/kameris-formats/storage_encoding.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/kameris-formats/binary_io.cpp;/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/tests/main.cpp") 
		  set(BOOST_INCLUDES_STRING "-I/home/vicente/libs/boost_1_64_0") 
		  set(CHECK_LINT_LOGFILE "/home/vicente/projects/BIOINFORMATICS/bio-samples/viral/kameris-backend/build/check_lint_log") 
		  						foreach(SOURCE_FILE ${PROJECT_SOURCES})
							execute_process(COMMAND clang-tidy "${SOURCE_FILE}" -- -I. -Iexternal ${BOOST_INCLUDES_STRING} --std=gnu++14
											OUTPUT_FILE "${CHECK_LINT_LOGFILE}"
											ERROR_FILE "${CHECK_LINT_LOGFILE}")
							execute_process(COMMAND	grep -Ev "(warnings.*generated\\.|Error while processing|Suppressed.*warnings|display errors from all non-system headers)"
											COMMAND perl external/colorgcc.pl
											INPUT_FILE "${CHECK_LINT_LOGFILE}")
						endforeach(SOURCE_FILE)