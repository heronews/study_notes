# setting.json
在CMakeLists.txt中添加`set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`,生成compile_commands.json文件
```
{
    "cmake.configureOnOpen": true,
    // 开启粘贴保存自动格式化
    "editor.formatOnPaste": false,
    "editor.formatOnType": false,
    "clangd.path": "/usr/bin/clangd",
    // Clangd 运行参数(在终端/命令行输入 clangd --help-list-hidden 可查看更多)
    "clangd.arguments": [
        // compile_commands.json 生成文件夹
        "--compile-commands-dir=${workspaceFolder}/build",
        // Clangd 日志
        "--log=error",
        // 全局补全
        "--all-scopes-completion",
        "--completion-style=bundled",
        // 在后台自动分析文件(基于 complie_commands，我们用CMake生成)
        "--background-index",
        // 启用 Clang-Tidy 以提供「静态检查」
        "--clang-tidy",
        // Clang-Tidy 静态检查的参数，指出按照哪些规则进行静态检查
        "--clang-tidy-checks=clang-*",
        // 默认格式化风格
        "--fallback-style=GNU",
        // 同时开启的任务数量
        "-j=8",
        // pch优化的位置(memory 或 disk，选择memory会增加内存开销，但会提升性能)
        "--pch-storage=memory",
        "--header-insertion=never"
    ],
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}/build/devel/lib/python3/dist-packages"
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}/build/devel/lib/python3/dist-packages"
    ]
}
```
