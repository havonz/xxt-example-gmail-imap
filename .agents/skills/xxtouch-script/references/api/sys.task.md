# sys.task

Purpose: Create a subprocess task

## Signature
```lua
task = sys.task(executable_file_path [, arguments...])
```

## Example
```lua
-- Simulate the following Shell command:
-- echo "hello world" | /usr/bin/gzip -fc | /usr/bin/gzip -dfc

local comp_tsk = sys.task(jbroot('/usr/bin/gzip'), '-fc')    -- Create the compression task.
local decomp_tsk = sys.task(jbroot('/usr/bin/gzip'), '-dfc') -- Create the decompression task.

decomp_tsk:set_stdin(comp_tsk:stdout()) -- Set the decompression task input stream to the compression task output stream.

decomp_tsk:launch() -- Start the decompression task.
comp_tsk:launch() -- Start the compression task.

comp_tsk:stdin():write("hello world") -- Write data to the compression task input stream.
comp_tsk:stdin():wclose() -- Close the write end of the compression task input stream, indicating that the input stream has ended.

comp_tsk:wait_until_exit() -- Wait for the compression task to finish.
decomp_tsk:wait_until_exit() -- Wait for the decompression task to finish.

nLog(decomp_tsk:stdout():read()) -- Read the decompression task output stream. Outputs "hello world".
```

## Non-blocking Output Read
```lua
local tsk = sys.task('/bin/echo', 'hello')
tsk:set_stdin('/dev/null')
tsk:launch()

local outbuf = {}
local errbuf = {}
local function drain_stream(stream, buf)
    local data = stream:read('nb')
    if data and #data > 0 then
        buf[#buf + 1] = data
    end
end

while tsk:is_running() do
    drain_stream(tsk:stdout(), outbuf)
    drain_stream(tsk:stderr(), errbuf)
    sys.msleep(100)
end
tsk:wait_until_exit()
drain_stream(tsk:stdout(), outbuf)
drain_stream(tsk:stderr(), errbuf)

if tsk:termination_status() == 0 then
    nLog(table.concat(outbuf))
else
    nLog(table.concat(errbuf))
end
```

## Common Task Object Methods
- `:launch()`: starts the task asynchronously.
- `:wait_until_exit()`: synchronously waits for the task to end. Even if `:is_running()` already returns `false`, call it once to avoid zombie processes.
- `:set_stdin(input_stream)` / `:stdin()`: sets or gets standard input. The input stream can be `"std"`, `"/dev/null"`, a file path, or a pipe object. It cannot be set after the task starts.
- `:set_stdout(output_stream)` / `:stdout()`: sets or gets standard output.
- `:set_stderr(error_stream)` / `:stderr()`: sets or gets standard error.
- `:set_work_dir(directory)` / `:work_dir()`: sets or gets the working directory. It cannot be set after the task starts.
- `:set_env(environment_variable_table)` / `:env()`: sets or gets environment variables.
- `:pid()`: gets the process ID. Returns `0` before the task starts.
- `:is_running()`: determines whether the task is still running.
- `:interrupt()` / `:terminate()` / `:kill()`: sends SIGINT, SIGTERM, and SIGKILL respectively.
- `:termination_status()`: gets the exit status. Returns `nil, error_message` if the task has not ended.
- `:termination_reason()`: gets the termination reason. Returns `nil, error_message` if the task has not ended.

## Pipe Object Methods
- `:read()`: reads data that is already ready.
- `:read('nb')`: non-blocking read of data that is already ready.
- `:write(data)`: writes data.
- `:wclose()`: closes the write end. Returns `true` on success, or `false, error_message` on failure.
- `:rclose()`: closes the read end. Returns `true` on success, or `false, error_message` on failure.

## Parameters
- executable_file_path
    string
- arguments...
    string, optional variadic parameters. Defaults to none.

## Returns
- task
    task object used to control the subprocess.

## Notes
Creates a subprocess task and returns a task object.
If you do not want to block all threads while waiting for the task to finish, repeatedly call the task object's `:is_running()` to check whether it is still running. After it ends, call `:wait_until_exit()` once more to confirm that the task has terminated.
