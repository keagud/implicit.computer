+++
title =  "A Handy Pattern for Rust Errors"
slug =  "rust-errors"
date = 2024-03-29
[taxonomies]
tags = ["programming", "rust" ,  "100DaysToOffload"]
+++


Here's a nifty pattern I use for making Rust error handling more ergonomic. Feel free to skip to the code at the end if you're already well versed in Rust error types.

For everyone else, a quick primer/refresher - Rust takes a cue from the functional side of the isle for its error handling approach. In a nutshell: if an operation *should* produce a type T, but it might also fail altogether, the Rusty idiom is to use the `Result` enum type. For example, what's the correct return type for the standard library function `fs::read_to_string`,  which reads the contents of a file as a string and returns it? Not just `String` --  what if the file isn't there, or doesn't have the right permissions, or its contents are invalid UTF-8 and so can't be represented as a `String`? 

The solution is to use the type `Result<String, io::Error>`[^1]. Either you get the string you asked for or an `io::Error` that represents why the action failed, so you can handle errors without jumping out of normal program flow in the way exception-based error handling requires.


Like a lot of Rust stuff, this is a very cool idea but can be fiddly in practice. Errors are values with types, so for a  function returning `Result<T, E>` any errors need to be *specifically* of type E. For example, this doesn't compile [^2]

```rust

use std::fs;
use std::io;
use reqwest::blocking::get;

pub fn save_a_webpage() -> Result<(), io::Error> {
    let page_content = get("https://www.example.com")?.text()?;
    fs::write("/home/user/website.html", page_content)?;

    Ok(())
}

```

The type `reqwest::Error`  is from  [reqwest](https://docs.rs/reqwest/latest/reqwest/index.html), the predominant HTTP client library for Rust. It's a type for HTTP errors, and it's used in the `get` function because a network request could fail for network-y reasons like no connection, invalid URI, or something else it makes sense to have defined in the same crate. It isn't the same as `io::Error`, but this function might fail for network *or* local IO reasons - what if we don't have permission to write to  `/home/user`, or that directory doesn't exist at all?

You might define a new Error enum that includes both those types as varients: 

```rust

pub enum NetworkOrIoError{
 IoError(std::io::Error),
 NetworkError(reqwest::Error)
}

```

This has the advantage of giving callers the option to behave differently depending on error type, e.g. a `NetworkError` might trigger a retry but an `IoError` might not. But what if you also want to distinguish an error for malformed HTML - now you need another variant, and another branch in any pattern match blocks that operate on this type. In the early stages of a project this is a real pace killer, plus you'll inevitably not get it correct the first time and need to go back and try something else. 

The other approach is to use generic error types. `Box<dyn std::error::Error>` more or less means "a type that you know implements the `std::error::Error` trait, but you can't say anything else for sure", and in a return type it works with any sort of error. The [anyhow](https://docs.rs/anyhow/latest/anyhow/) crate provides the `anyhow::Error` type with a similar function. This lets you move fast and focus on the core control flow without distraction, but once the project matures and settles into something more stable it becomes frustratingly opaque for function callers and adds some friction to writing code that interfaces with the existing API. 

Here's my solution to this: an `error.rs` file containing this: 

```rust
pub type Error = Box<dyn std::error::Error + Sync + Send>;
pub type Result<T> = std::result::Result<T, crate::error::Error>;
```

And then in `lib.rs`:
```rust
pub mod error;
pub use error::{Error, Result};
```

Now you can use `crate::Error` as a generic error type (`crate::Result` is just a convenience alias).  When you hit the point where clarity is more important than velocity, you can swap out the definition of `crate::Error` for an actual enum type with appropriate variants, without needing to change a million function signatures to match. 


I'm pretty sure I did not invent this pattern, but I did independently re-derive it and I haven't really seen anyone else talk about it online. Possibly this is because it's so obvious that no one considers it worth discussion, but I thought I'd share on the off chance someone finds it helpful. 



---
[^1]: The actual [docs](https://doc.rust-lang.org/nightly/std/fs/fn.read_to_string.html) give a return type of `io::Result<String>`, but that's just a more concise alias. 

[^2]: If you're not familiar with the question mark operator, it's just syntactic sugar for returning an error early.
