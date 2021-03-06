# kameris-formats

[![Travis](https://travis-ci.org/stephensolis/kameris-formats.svg?branch=master)](https://travis-ci.org/stephensolis/kameris-formats)
[![Codacy](https://api.codacy.com/project/badge/Grade/a61ec5a7cb51408a8682da2d2f574eba)](https://www.codacy.com/app/stephensolis/kameris-formats)
[![Codebeat](https://codebeat.co/badges/6bbcb148-37b7-40d7-ba5e-21340541ada8)](https://codebeat.co/projects/github-com-stephensolis-kameris-formats-master)
[![Codeclimate](https://api.codeclimate.com/v1/badges/10a65d7201ebbfb56ab5/maintainability)](https://codeclimate.com/github/stephensolis/kameris-formats/maintainability)

These are implementations of readers and writers for the file formats used by [kameris-backend](https://github.com/stephensolis/kameris-backend), for the following languages:

| Language    | Location                                                                                           | Notes                                                           |
|-------------|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| C++         | [`cpp/`](https://github.com/stephensolis/kameris-formats/tree/master/cpp)                 | Header-only, requires [libkameris](https://github.com/stephensolis/kameris-backend/tree/master/libkameris) |
| Python      | [`python/`](https://github.com/stephensolis/kameris-formats/tree/master/python)           | On PyPI: [![PyPI version](https://badge.fury.io/py/kameris-formats.svg)](https://badge.fury.io/py/kameris-formats) |
<!---
| Mathematica | [`mathematica/`](https://github.com/stephensolis/kameris-formats/tree/master/mathematica) | |
| MATLAB      | [`matlab/`](https://github.com/stephensolis/kameris-formats/tree/master/matlab)           | |
--->

---

## File formats

There are two different file formats used to store program output. `repr` mode generates files with the extension `.mm-repr` and `dist` mode generates files with the extension `.mm-dist`.

Data is always stored in little-endian format. All header values except the signature are unsigned integers.

`element_type` is a common enum used to specify the type of the stored data. Its values are as follows:

| Value | Name      | Element size (bytes) | Description                              |
|-------|-----------|----------------------|------------------------------------------|
| 0     | `uint8`   | 1                    | 8-bit unsigned integer                   |
| 1     | `uint16`  | 2                    | 16-bit unsigned integer                  |
| 2     | `uint32`  | 4                    | 32-bit unsigned integer                  |
| 3     | `uint64`  | 8                    | 64-bit unsigned integer                  |
| 4     | `float32` | 4                    | IEEE 754 single-precision floating point |
| 5     | `float64` | 8                    | IEEE 754 double-precision floating point |

## `repr` format (`.mm-repr` files)

### Header

| Start | End  | Size (bytes)  | Name         | Description                                                               |
|-------|------|---------------|--------------|---------------------------------------------------------------------------|
| 0x00  | 0x05 | 6             | `signature`  | File signature, always "MMREPR"                                           |
| 0x06  | 0x06 | 1             | `version`    | Always 0                                                                  |
| 0x07  | 0x07 | 1             | `is_sparse`  | Whether the matrices are sparse (0 or 1)                                  |
| 0x08  | 0x08 | 1             | `key_type`   | The type of matrix keys as an `element_type`, unused if `is_sparse` is 0  |
| 0x09  | 0x09 | 1             | `value_type` | The type of matrix values as an `element_type`                            |
| 0x0A  | 0x11 | 8             | `count`      | Number of matrices                                                        |
| 0x12  | 0x19 | 8             | `rows`       | Number of rows for each matrix                                            |
| 0x1A  | 0x21 | 8             | `columns`    | Number of columns for each matrix                                         |
| 0x22  |      | 8 * `count`   | `sizes`      | (**Only if `is_sparse` is 1**) Number of non-zero entries for each matrix |

If the sparse flag is not set, the following `count` * `rows` * `columns` * (size for `value_type`) bytes are the entries, in row-major order, for each of the `count` matrices, one after the other.

If the sparse flag is set, each of the `count` matrices, one after the other, is stored as (the matrix size from `sizes`) * (size for `key_type`) * (size for `value_type`) bytes which are (the matrix size from `sizes`) pairs of key followed by value. The order of keys is unspecified.

## `dist` format (`.mm-dist` files)

### Header

| Start | End  | Size (bytes)  | Name         | Description                                    |
|-------|------|---------------|--------------|------------------------------------------------|
| 0x00  | 0x05 | 6             | `signature`  | File signature, always "MMDIST"                |
| 0x06  | 0x06 | 1             | `version`    | Always 0                                       |
| 0x07  | 0x07 | 1             | `value_type` | The type of matrix values as an `element_type` |
| 0x08  | 0x0F | 8             | `size`       | Number of rows = columns of the matrix         |

The following (`size` * (`size` - 1)) / 2 * (size for `value_type`) bytes are the entries **above** the main diagonal, in row-major order, of the matrix. The matrix is assumed to be symmetric and have zeros on the main diagonal.

---

## License ![License](http://img.shields.io/:license-mit-blue.svg)

    The MIT License (MIT)

    Copyright (c) 2017 Stephen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
