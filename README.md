# ![Program icon](assets/logo.ico) PyBot

A general purpose Discord bot using [`Discord.py`](https://github.com/Rapptz/discord.py). This can be used to play music from YouTube and compile code snippets. It is great for prototyping ideas, or testing concepts on-the-fly with very little effort. It supports almost every programing language you could name.

## 🧑‍🏫 Usage

To use the bot you need to first add it to your server (currently you have to host it yourself). Then you can use the following commands:

### 🎵 Music

1. Play music from YouTube

    ```nim
    $play <song name> or <song url>
    $p <song name> or <song url>
    ```

2. Show current playing song

    ```nim
    $nowplaying
    $np
    $now_playing
    ```

3. Pause music

    ```nim
    $pause
    ```

4. Resume music

    ```nim
    $resume
    $unpause
    ```

5. Display queue and playlist

    ```nim
    $queue
    $q
    $playlist
    ```

6. Skip to next song

    ```nim
    $skip
    $s
    ```

7. Join and move to your current voice channel

    ```nim
    $join
    ```

### 👨‍💻 Code compilation

 1. Show supported programming languages

    ```nim
    $languages
    ```

 2. Show supported compilers for a specific language

    ```nim
    $compilers <language name>
    ```

 3. Compile and run code

    ```nim
        $compile [language] [compiler flags(optional)]
        [args (optional)]
        ```[language name or alias (optional)]

        <your code>

        ```
        [stdin (optional)]
    ```

    Examples:

    - Example 1

        ```nim
            $compile python
            ```python
            print("Hello World")
            ```
        ```

    - Example 2

        ```nim
            $compile c
            ```c
            #include <stdio.h>
            
            int main(void) {
                printf("Hello World\n");
                return 0;
            }
            ```
        ```

    - Example 3

        ```nim
            $compile c++ -Wall -Wextra
            command line arguments

            ```c++
            #include <iostream>
            #include <string>

            int main(int argc, char *argv[]) {

                std::string user_name;
                std::cin >> user_name;
                std::cout << "Hello, " << user_name << "." << std::endl;

            return 0;
            }
            ```
            PyBot
        ```

## ⚠️ Limitations

Keep in mind that we're working in discord. This means, of course, that we have many operating restraints. Also the [`Compiler Explorer`](https://compiler-explorer.com/) API has some limitations.

## ⚖️ License

This project is under the [`MIT license`](https://choosealicense.com/licenses/mit/). Review it [here](LICENSE).

## ☁️ Hosting it yourself?

⚠️
Before hosting it you must consider some things. In my part everything is fine since I released it under the [`MIT license`](LICENSE), but i suggest to check [`YouTube terms of service`](https://www.youtube.com/t/terms) first, if you want to use the implemented music service, since it's hosted by YouTube.

### Quick start

Start by cloning the repository and navigating to the folder.

```console
git clone https://github.com/detjonmataj/PyBot-Discord.git
cd PyBot
```

#### Prerequisites

- Python Python 3.10.5
  - Check [`Discord.py`](https://discordpy.readthedocs.io/en/latest/api.html#discord-py-version) for more information

- Install Python Modules specified in the [`requirements.txt`](requirements.txt) file

    ```shell
    pip install -r requirements.txt
    ```

- Rename .env.example to .env and fill the required fields

#### Run the bot

##### 🪟 Windows

```shell
py -3.10-64 bot.py
```

##### 🐧 Linux and 🍎 MacOS

```shell
python3 bot.py
```

## 📝 Development Milestones and Future Plans

- [x] Implement music player
- [x] Implement code compilation and execution
- [ ] Improve music player and code compilation commands
- [ ] New complers and languages support from wandbox.org API
- [ ] Use Lavalink or Wavelink instead for music player
- [ ] Implement server management commands
- [ ] Implement logging system
- [ ] Implement Caching for music and code compilation
- [ ] Implement games
- [ ] Implement code contests from my `Contester++` API
- [ ] Interact with different APIs for improving productivity (Jira, Gitlab, Github, Azure Devops, Nagios, etc.)
- [ ] Host the the bot to be used publicly
- [ ] Refactor code
- [ ] More ideas before Final Release
- [ ] Final Release
- [ ] Discontinued
