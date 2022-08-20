---
template: overrides/main.html
---
# Appendix

This section contains topics that don't fit anywhere else in the documentation.

#### Add CLI to PATH


=== "bash / zsh"

    Step 1. Create a directory for local binaries:

    ```sh
    mkdir -p ~/bin
    ```
    
    Step 2. Move the `nitro` executable there:

    ```sh
    mv ~/path/to/nitro ~/bin
    ```

    Step 3. Append this line to your `~/.bashrc` or `~/.zshrc` file:

    ```sh
    export PATH=~/bin:${PATH}
    ```

    Step 4. Exit and open a new terminal.

    Step 5. Verify if the `nitro` command works:

    ```sh
    nitro version
    ```


=== "Windows"

    Step 1. Move `nitro.exe` to a local directory, say, `C:\Users\MyUsername\bin`
    
    Step 2. Add `C:\Users\MyUsername\bin` to your system's `Path`. [See walkthrough](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/).

    Step 3. Open a new Command Prompt.

    Step 4. Verify if the `nitro` command works:

    ```sh
    nitro version
    ```

