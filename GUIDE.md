# Guide

**NOTE**: If you take a pull request with a wrong format, this request will be rejected.

We are using [Github Actions](README.md) to render [README.md](README.md) automatically. For neat file-arrangement and auto-render without errors, you should add files in correct format.

#### Papers

For papers, you need to put it into [Papers](Papers/) dir then go to the sub-dir named by task. If there is no one, create it. The file name should be `[00 CONF]PAPER_NAME.pdf`.

* Example:

[[18 ECCV]LSQ++.pdf](Papers/Quantization/%5B16%20ECCV%5DLSQ.pdf) is put into `./Papers/Quantization/[18 ECCV]LSQ++.pdf`.


#### Codes

If you have a paper-related code, add it into the [Codes](Codes/) dir. Name the dir with the same name as paper (just remove the `[00 CONF]` prefix and `.pdf` suffix). If the code is hosted on other git repositories, you should use `git submodule` other than directly upload it.

If the code is independent with any papers, the only need is put it into correct directory.

* Example:

[LSQ](Codes/LSQ) is a `git submodule` which points to [this repo](github.com), while [LSQ-Python](Codes/Quantization/LSQ-Python) is a git submodule which is put in the `Quantization` sub-dir, indicating it is a paper-indepedent work.


#### Tutorials

This is generally the same with previous sections. Put into sub-dir, use `git submodule` if it has one.

