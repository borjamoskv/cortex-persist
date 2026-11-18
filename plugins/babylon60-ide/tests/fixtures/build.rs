use std::{env, fs, io::ErrorKind, process::Command};

fn main() {
    let root = env::var("CARGO_MANIFEST_DIR").unwrap();
    let err = fs::write(format!("{root}/src/lib.rs"), "overwritten").unwrap_err();
    assert!(matches!(err.kind(), ErrorKind::PermissionDenied | ErrorKind::ReadOnlyFilesystem));
    let output = Command::new("/bin/sh")
        .args(["-c", "printf bad > src/lib.rs"])
        .output().unwrap();
    assert!(!output.status.success());
    println!("cargo:warning=NEMESIS_BUILD_WRITE_DENIED: {err}; {}",
        String::from_utf8_lossy(&output.stderr));
    fs::write(format!("{}/build-output", env::var("OUT_DIR").unwrap()), "allowed").unwrap();
}
