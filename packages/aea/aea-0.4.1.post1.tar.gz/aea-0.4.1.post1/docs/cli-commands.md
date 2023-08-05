# CLI commands

| Command                                     | Description                                                                  |
| ------------------------------------------- | ---------------------------------------------------------------------------- |
| `add connection/protocol/skill [public_id]` | Add connection, protocol, or skill, with `[public_id]`, to the AEA. `add --local` to add from local `packages` directory. |
| `add-key fetchai/ethereum file`             | Add a private key from a file.	                                             |
| `create NAME`                               | Create a new aea project called `[name]`.                                    |
| `config get [path]`                         | Reads the config specified in `[path]` and prints its target.                |
| `config set [path] [--type TYPE]`           | Sets a new value for the target of the `[path]`. Optionally cast to type.    |
| `delete NAME`                               | Delete an aea project. See below for disabling a resource.                   |
| `fetch PUBLIC_ID`                           | Fetch an aea project with `[public_id]`. `fetch --local` to fetch from local `packages` directory. |
| `fingerprint c/p/s [public_id]`             | Fingerprint connection, protocol, or skill, with `[public_id]`.              |
| `freeze`                                    | Get all the dependencies needed for the aea project and its components.      |
| `gui`                                       | Run the GUI.                                                                 |
| `generate-key fetchai/ethereum/all`         | Generate private keys. The AEA uses a private key to derive the associated public key and address. |
| `generate-wealth fetchai/ethereum`          | Generate wealth for address on test network.                                 |
| `get-address fetchai/ethereum`              | Get the address associated with the private key.                             |
| `get-wealth fetchai/ethereum`               | Get the wealth associated with the private key.                              |
| `install [-r <requirements_file>]`          | Install the dependencies. (With `--install-deps` to install dependencies.)   |
| `init`                                      | Initialize your AEA configurations. (With `--author` to define author.)      |
| `launch [path_to_agent_project]...`         | Launch many agents at the same time.                                                          |
| `list protocols/connections/skills`         | List the installed resources.                                                |
| `login USERNAME [--password password]`      | Login to a registry account with credentials.                                |
| `publish`                                   | Publish the AEA to registry. Needs to be executed from an AEA project.`publish --local` to publish to local `packages` directory. |
| `push connection/protocol/skill [public_id]`| Push connection, protocol, or skill with `[public_id]` to registry.	`push --local` to push to local `packages` directory. |
| `remove connection/protocol/skill [name]`   | Remove connection, protocol, or skill, called `[name]`, from AEA.            |
| `run {using [connections, ...]}`            | Run the AEA on the Fetch.ai network with default or specified connections.   |
| `search protocols/connections/skills`       | Search for components in the registry. `search --local protocols/connections/skills [--query searching_query]` to search in local `packages` directory. |
| `scaffold connection/protocol/skill [name]` | Scaffold a new connection, protocol, or skill called `[name]`.               |
| `-v DEBUG run`                              | Run with debugging.                                                          |

<!--
Command  | Description
---------| -----------------------------------------------------------------
`deploy {using [connection, ...]}`  | Deploy the AEA to a server and run it on the Fetch.ai network with default or specified connections.
 -->

<div class="admonition tip">
  <p class="admonition-title">Tip</p>
  <p>You can also disable a resource without deleting it by removing the entry from the configuration but leaving the package in the skills namespace.</p>
</div>

<div class="admonition tip">
  <p class="admonition-title">Tip</p>
  <p>You can skip the consistency checks on the AEA project by using the flag `--skip-consistency-check`. E.g. `aea --skip-consistency-check run` will bypass the fingerprint checks.</p>
</div>

<br />
