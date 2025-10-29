+++
title = "Simple Systemd Services"
slug = "simple-systemd-services"
date = 2025-10-29

[taxonomies]
tags = [ "systemd", "linux", "sysadmin",]
+++

Here's a template for server daemon programs I've found useful.
The example daemon implementation is in Rust because that's what I like to use for these things, but the idea is language-agnostic.


```rust
use std::env::args;
use std::fs;
use std::path;
use std::str::FromStr;
use serde;
use toml;

#[derive(Debug, serde::Deserialize)]
struct MyConfig {
field1: String,
field2: u32
// ...
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let fp = args().nth(1).unwrap();

    let p = path::PathBuf::from_str(fp.as_str())?;

    let config: MyConfig = toml::from_str(&fs::read_to_string(p.as_path())?)?;

    // ... the code to do The Thing using values from the config
 
}
```

And the template for a service unit file:

```ini
[Unit]
Description=myservice
After=network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/myservice /etc/myservice/config.toml
Restart=on-failure
RestartSec=5
User=www-data
Group=www-data

[Install]
WantedBy=multi-user.target
```

The basic layout is:
1. Write a program that takes a single argument, a path to a config file. I like to use toml, but you could do json or even something funky and bespoke if you want
2. Copy the program executable to `/usr/local/bin/` and the config file to `/etc/myservice/`
3. Complete the  service unit template and stick it in `/etc/systemd/system/`, e.g. as `myservice.service`
4. Run `sudo systemctl enable --now myservice`

Of course the exact service parameters may not be what you want, but I like to use this as a jumping off point I can tack more options onto later as they become needed.
