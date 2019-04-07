# PlayFair Encryption and Decryption

This repository contains a PlayFair class that can be used to encrypt/decrypt messages using the PlayFair cipher.

## Functionality

The functionalities specified below assume that all code is executed and variables can be reused later.

- import the playfair module:

  ```python
  from playfair import PlayFair
  ```

- Key generation based on keying material supplied:

  ```python
  playfair = PlayFair().generate_key("insert keying material here")
  ```

  The key (5x5 matrix/tableau) can be printed by using:

  ```python
  playfair.print_tableau()
  ```

- Encryption of messages or files provided (after a key has been generated).
  This also includes 'passthrough' of non-encryptable characters like punctuation:

  ```python
  cipher_text = playfair.encrypt("plaintext message")
  cipher_text = playfair.encrypt_file("path/to/plaintext/file")
  ```

- Decryption of messages or files provided (after a key has been generated).
  This also includes 'passthrough' of non-decryptable characters like punctuation:

  ```python
  plain_text = playfair.decrypt("ciphertext message")
  plain_text = playfair.decrypt_file("path/to/ciphertext/file")
  ```

- The substitute char (character that is substituted), substitute by (character that the substitube char is substituted by) and padding char (character that is used for padding) can be read and changed.

  substitute_char defaults to 'j'.  
  substitute_by defaults to 'i'.  
  padding_char defaults to 'x'.

  ```python
  substitute_char = playfair.substitute_char
  playfair.substitute_char = "some char"
  substitute_by = playfair.substitute_by
  playfair.substitute_by = "some char"
  padding_char = playfair.padding_char
  playfair.padding_char = "some char"
  ```

- All or nearly all functions include input verification and report any errors or warnings as they occur.

## Future work

- Add ability to brute force PlayFair keys (either the rules, the keying material or the resulting tableau).
  This brute force attempt can use the PlayFair class to perform encryption/decryption of a chosen message,
  thus has access to both the original message and the ciphertext of its choosing
