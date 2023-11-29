# pip-gpt

Install Python libraries to your custom GPTs

## Usage

#### Clone the repository
```
git clone https://github.com/dceluis/pip-gpt.git
cd pip-gpt
```

#### Run
```
python generate.py ultralytics==8.0.220
```
This will create a `bundle.zip` file in the current directory.

#### Upload `bundle.zip` to your custom GPT.

#### Finally, prepend the following instructions to your GPT prompt:

```
When starting the conversation, and before attempting code execution, you will:
1. Unzip the bundle file (which is available in your current workspace) to the ./pip_gpt folder.
2. Read each install script in ./pip_gpt/install_scripts and print the file contents.
3. Run each install script contents, run the installation silently (don't output installation success messages).
```

## Caveats

1. This method fails often. The good part is that GPT-4 will try to correct what
   went wrong, the bad part is that it's a bad user experience anyway.
2. It takes a while. You will be adding at least 20 seconds of delay to your
   first response while the install scripts are extracted and run.
3. It doesn't add dependencies. I have not yet found a clean way of only adding
   dependencies not already present in the GPT host.

## TODO

- [ ] Merge install scripts into one.
- [ ] Specify the platform so that it matches the GPTs host machine.
- [ ] Include pruned dependency tree.
