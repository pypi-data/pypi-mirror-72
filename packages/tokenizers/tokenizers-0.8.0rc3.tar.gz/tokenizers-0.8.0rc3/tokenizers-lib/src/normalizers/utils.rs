use crate::tokenizer::{NormalizedString, Normalizer, Result};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
/// Allows concatenating multiple other Normalizer as a Sequence.
/// All the normalizers run in sequence in the given order against the same NormalizedString.
pub struct Sequence {
    normalizers: Vec<Box<dyn Normalizer>>,
}

impl Sequence {
    pub fn new(normalizers: Vec<Box<dyn Normalizer>>) -> Self {
        Self { normalizers }
    }
}

#[typetag::serde]
impl Normalizer for Sequence {
    fn normalize(&self, mut normalized: &mut NormalizedString) -> Result<()> {
        for normalizer in &self.normalizers {
            normalizer.normalize(&mut normalized)?;
        }
        Ok(())
    }
}

#[derive(Serialize, Deserialize)]
/// Lowercases the input
pub struct Lowercase;
#[typetag::serde]
impl Normalizer for Lowercase {
    fn normalize(&self, normalized: &mut NormalizedString) -> Result<()> {
        normalized.lowercase();
        Ok(())
    }
}
