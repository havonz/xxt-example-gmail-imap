# coreml.tokenizer.module

Purpose: Text tokenizer module

The tokenizer is only responsible for encoding strings into token IDs or decoding token IDs back into text. Model inference is handled by CoreML or ONNX Runtime.

## Signature
```lua
tokenizer, error_message = coreml.new_text_tokenizer(options)
encoded_result, error_message = tokenizer:encode(text [, options])
encoded_result, error_message = tokenizer:encode_batch(text_array [, options])
text, error_message = tokenizer:decode(ids)
text_array, error_message = tokenizer:decode_batch(batch_ids)
vocab_size = tokenizer:vocab_size()
context_length = tokenizer:context_length()
```

## Creation Examples
```lua
local tokenizer = assert(coreml.new_text_tokenizer({
    type = "wordpiece",
    vocab_path = XXT_HOME_PATH.."/models/demo/vocab.txt",
    context_length = 52,
}))

local input_ids = assert(tokenizer:encode("stars", {
    output = "MLMultiArray",
    data_type = "int32",
}))
```

ONNX Runtime text model:

```lua
local ort = require("onnxruntime")

local input_ids = assert(tokenizer:encode("stars", {
    output = "ort_tensor",
    data_type = "int64",
}))
```

Structured output:

```lua
local item = assert(tokenizer:encode("stars", {
    output = "table",
    return_attention_mask = true,
    return_token_type_ids = true,
}))

print(item.input_ids, item.attention_mask, item.length)
```

## Creation Parameters
```lua
tokenizer, error_message = coreml.new_text_tokenizer({
    type = tokenizer_type,
    vocab_path = vocab_path,
    merges_path = merges_file_path,
    model_path = SentencePiece_model_path,
    pattern = regular_expression,
    context_length = context_length,
    do_lower_case = whether_to_lowercase,
    vocab_limit = vocabulary_limit,
    clean_text = whether_to_clean_text,
    add_bos = whether_to_add_beginning_token,
    add_eos = whether_to_add_ending_token,
    bos_token = beginning_token_text,
    eos_token = ending_token_text,
    pad_token = padding_token_text,
    unk_token = unknown_token_text,
})
```

Shortcut constructors:
- `coreml.new_wordpiece_tokenizer(opts_or_vocab_path)`
- `coreml.new_bpe_tokenizer(opts)`
- `coreml.new_sentencepiece_tokenizer(opts)`
- `coreml.new_regex_tokenizer(opts)`
- `coreml.new_byte_tokenizer(opts)`
- `coreml.new_whitespace_tokenizer(opts)`
- `coreml.new_character_tokenizer(opts)`

`coreml.is_text_tokenizer(value)` checks the object type.

## Tokenizer Types
- `wordpiece` / `bert` / `cn_clip`
- `bpe` / `gpt2_bpe` / `clip_bpe`
- `sentencepiece` / `spm`
- `regex` / `pattern`
- `byte` / `bytes`
- `whitespace` / `space`
- `character` / `char`

Default: `wordpiece`. If the first argument to `new_text_tokenizer(...)` is not a table, it is handled as the `wordpiece` shortcut constructor, equivalent to `new_wordpiece_tokenizer(vocab_path)`.

## Creation Parameter Rules
- `vocab_path`: vocabulary file path.
- `merges_path`: BPE merges file path.
- `model_path`: SentencePiece `.model` path.
- `pattern`: regular expression used by the regex tokenizer.
- `context_length`: fixed output length.
- `do_lower_case`: whether to lowercase before encoding.
- `vocab_limit`: commonly used by WordPiece to limit the vocabulary size.
- `clean_text`: basic cleaning before tokenization.
- `add_bos` / `add_eos`: whether to append beginning / ending tokens.
- `bos_token` / `eos_token` / `pad_token` / `unk_token`: special token text.

Type defaults and required fields:
- `wordpiece`: accepts a `vocab_path` string directly or a table; requires `vocab_path`; defaults to `context_length = 52`, `do_lower_case = true`, `vocab_limit = 21128`; vocabulary must contain `[PAD]`, `[UNK]`, `[CLS]`, `[SEP]`.
- `bpe`: only accepts a table; requires `vocab_path` and `merges_path`; defaults to `context_length = 77`, `do_lower_case = false`, `clean_text = false`, `add_bos = false`, `add_eos = false`.
- `sentencepiece`: only accepts a table; requires at least one of `vocab_path` or `model_path`; defaults to `context_length = 77`, `do_lower_case = false`, `clean_text = true`, `bos_token = "<s>"`, `eos_token = "</s>"`, `pad_token = "<pad>"`, `unk_token = "<unk>"`.
- `regex`: only accepts a table; requires `vocab_path` and `pattern`; defaults to `context_length = 77`, `do_lower_case = false`, `clean_text = true`.
- `whitespace` / `character` / `byte`: only accepts a table; requires `vocab_path`; defaults to `context_length = 77`, `do_lower_case = false`, `clean_text = true`.

Selection:
- `vocab.txt + WordPiece`: `wordpiece`, suitable for BERT and CN-CLIP.
- `vocab.json + merges.txt`: `bpe`, suitable for GPT-2/CLIP BPE style.
- `.vocab` or `.model`: `sentencepiece`.
- Simple rule-based token splitting: `regex`, `whitespace`, `character`, `byte`.

## Object Methods
```lua
encoded_result, error_message = tokenizer:encode(text [, options])
encoded_result, error_message = tokenizer:encode_batch(text_array [, options])

text, error_message = tokenizer:decode(ids)
text_array, error_message = tokenizer:decode_batch(batch_ids)

vocab_size = tokenizer:vocab_size()
context_length = tokenizer:context_length()
```

`decode(ids)` accepts a Lua array, `MLMultiArray`, ORT tensor, or any tensor-like userdata implementing `shape()` and `to_table()`. Use `decode_batch()` when passing batch data.

## Encoding Options
```lua
{
    output = "table" or "MLMultiArray" or "ort_tensor",
    data_type = data_type,
    pair_text = paired_text_or_paired_text_array,
    max_length = max_length,
    padding = padding_strategy,
    truncation = truncation_strategy,
    return_attention_mask = whether_to_return_attention_mask,
    return_token_type_ids = whether_to_return_token_type_ids,
    return_special_tokens_mask = whether_to_return_special_tokens_mask,
}
```

Rules:
- `output` defaults to `"MLMultiArray"`, suitable for feeding directly into CoreML.
- `output = "table"` is for debugging or compatibility with old scripts.
- `output = "ort_tensor"` is suitable for ONNX Runtime; `require("onnxruntime")` must be called first.
- The legacy field `multi_array_output` is supported for compatibility; new code should use `output`.
- `pair_text` for `encode_batch()` can be either a single string or a string array with the same length as the batch.

`data_type`:
- `output = "MLMultiArray"`: optional `"int32"`, `"float32"`, `"float16"`, `"double"`; default `"int32"`; `"float64"` is an alias for `"double"`.
- `output = "ort_tensor"`: optional `"float16"`, `"float32"`, `"uint8"`, `"int8"`, `"int32"`, `"int64"`, `"double"`, `"bool"`; default `"int64"`.

`padding` / `truncation`:
- `padding = true` is equivalent to `"max_length"`; `false` is equivalent to `"do_not_pad"`.
- `truncation = true` is equivalent to `"longest_first"`; `false` is equivalent to `"do_not_truncate"`.

## Structured Return
If any of the following fields is `true`, `encode()` / `encode_batch()` returns a structured table instead of a bare token sequence:
- `return_attention_mask`
- `return_token_type_ids`
- `return_special_tokens_mask`

Structured fields:
- `input_ids`
- `length`
- `attention_mask`
- `token_type_ids`
- `special_tokens_mask`

Batch Rules:
- When `output = "table"`, each sample keeps its own length.
- When `output = "MLMultiArray"` / `"ort_tensor"`, the batch is padded into a regular matrix.

## Usage Guidance
- Create the tokenizer once and reuse it; do not reconstruct it for every encoding.
- When model behavior is wrong, first check whether the tokenizer type, vocabulary, special tokens, and `context_length` match training.
- `WordPiece` is currently the most complete and stable. BPE/SentencePiece target on-device encoding compatibility and do not promise to replicate every detail of the upstream ecosystems.
