extern crate tokenizers as tk;

use super::error::{PyError, ToPyResult};
use super::utils::Container;
use pyo3::exceptions;
use pyo3::prelude::*;
use pyo3::types::*;
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use tk::tokenizer::Result;

#[pyclass(dict, module = "tokenizers.decoders")]
pub struct Decoder {
    pub decoder: Container<dyn tk::tokenizer::Decoder>,
}
#[pymethods]
impl Decoder {
    #[staticmethod]
    fn custom(decoder: PyObject) -> PyResult<Self> {
        let decoder = PyDecoder::new(decoder)?;
        Ok(Decoder {
            decoder: Container::Owned(Box::new(decoder)),
        })
    }

    fn __getstate__(&self, py: Python) -> PyResult<PyObject> {
        let data = self
            .decoder
            .execute(|decoder| serde_json::to_string(&decoder))
            .map_err(|e| {
                exceptions::Exception::py_err(format!(
                    "Error while attempting to pickle Decoder: {}",
                    e.to_string()
                ))
            })?;
        Ok(PyBytes::new(py, data.as_bytes()).to_object(py))
    }

    fn __setstate__(&mut self, py: Python, state: PyObject) -> PyResult<()> {
        match state.extract::<&PyBytes>(py) {
            Ok(s) => {
                self.decoder =
                    Container::Owned(serde_json::from_slice(s.as_bytes()).map_err(|e| {
                        exceptions::Exception::py_err(format!(
                            "Error while attempting to unpickle Decoder: {}",
                            e.to_string()
                        ))
                    })?);
                Ok(())
            }
            Err(e) => Err(e),
        }
    }

    fn decode(&self, tokens: Vec<String>) -> PyResult<String> {
        ToPyResult(self.decoder.execute(|decoder| decoder.decode(tokens))).into()
    }
}

#[pyclass(extends=Decoder, module = "tokenizers.decoders")]
pub struct ByteLevel {}
#[pymethods]
impl ByteLevel {
    #[new]
    fn new() -> PyResult<(Self, Decoder)> {
        Ok((
            ByteLevel {},
            Decoder {
                decoder: Container::Owned(Box::new(tk::decoders::byte_level::ByteLevel::default())),
            },
        ))
    }
}

#[pyclass(extends=Decoder, module = "tokenizers.decoders")]
pub struct WordPiece {}
#[pymethods]
impl WordPiece {
    #[new]
    #[args(kwargs = "**")]
    fn new(kwargs: Option<&PyDict>) -> PyResult<(Self, Decoder)> {
        let mut prefix = String::from("##");
        let mut cleanup = true;

        if let Some(kwargs) = kwargs {
            if let Some(p) = kwargs.get_item("prefix") {
                prefix = p.extract()?;
            }
            if let Some(c) = kwargs.get_item("cleanup") {
                cleanup = c.extract()?;
            }
        }

        Ok((
            WordPiece {},
            Decoder {
                decoder: Container::Owned(Box::new(tk::decoders::wordpiece::WordPiece::new(
                    prefix, cleanup,
                ))),
            },
        ))
    }
}

#[pyclass(extends=Decoder, module = "tokenizers.decoders")]
pub struct Metaspace {}
#[pymethods]
impl Metaspace {
    #[new]
    #[args(kwargs = "**")]
    fn new(kwargs: Option<&PyDict>) -> PyResult<(Self, Decoder)> {
        let mut replacement = '▁';
        let mut add_prefix_space = true;

        if let Some(kwargs) = kwargs {
            for (key, value) in kwargs {
                let key: &str = key.extract()?;
                match key {
                    "replacement" => {
                        let s: &str = value.extract()?;
                        replacement = s.chars().nth(0).ok_or(exceptions::Exception::py_err(
                            "replacement must be a character",
                        ))?;
                    }
                    "add_prefix_space" => add_prefix_space = value.extract()?,
                    _ => println!("Ignored unknown kwarg option {}", key),
                }
            }
        }

        Ok((
            Metaspace {},
            Decoder {
                decoder: Container::Owned(Box::new(tk::decoders::metaspace::Metaspace::new(
                    replacement,
                    add_prefix_space,
                ))),
            },
        ))
    }
}

#[pyclass(extends=Decoder, module = "tokenizers.decoders")]
pub struct BPEDecoder {}
#[pymethods]
impl BPEDecoder {
    #[new]
    #[args(kwargs = "**")]
    fn new(kwargs: Option<&PyDict>) -> PyResult<(Self, Decoder)> {
        let mut suffix = String::from("</w>");

        if let Some(kwargs) = kwargs {
            for (key, value) in kwargs {
                let key: &str = key.extract()?;
                match key {
                    "suffix" => suffix = value.extract()?,
                    _ => println!("Ignored unknown kwarg option {}", key),
                }
            }
        }

        Ok((
            BPEDecoder {},
            Decoder {
                decoder: Container::Owned(Box::new(tk::decoders::bpe::BPEDecoder::new(suffix))),
            },
        ))
    }
}

struct PyDecoder {
    class: PyObject,
}

impl PyDecoder {
    pub fn new(class: PyObject) -> PyResult<Self> {
        Ok(PyDecoder { class })
    }
}

#[typetag::serde]
impl tk::tokenizer::Decoder for PyDecoder {
    fn decode(&self, tokens: Vec<String>) -> Result<String> {
        let gil = Python::acquire_gil();
        let py = gil.python();

        let args = PyTuple::new(py, &[tokens]);
        match self.class.call_method(py, "decode", args, None) {
            Ok(res) => Ok(res
                .cast_as::<PyString>(py)
                .map_err(|_| PyError::from("`decode` is expected to return a str"))?
                .to_string()
                .map_err(|_| PyError::from("`decode` is expected to return a str"))?
                .into_owned()),
            Err(e) => {
                e.print(py);
                Err(Box::new(PyError::from("Error while calling `decode`")))
            }
        }
    }
}

impl Serialize for PyDecoder {
    fn serialize<S>(&self, _serializer: S) -> std::result::Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        Err(serde::ser::Error::custom(
            "Custom PyDecoder cannot be serialized",
        ))
    }
}

impl<'de> Deserialize<'de> for PyDecoder {
    fn deserialize<D>(_deserializer: D) -> std::result::Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        unimplemented!("PyDecoder cannot be deserialized")
    }
}
