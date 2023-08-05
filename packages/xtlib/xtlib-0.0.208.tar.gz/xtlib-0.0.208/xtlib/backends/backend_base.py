#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_base.py: provides a baseclass for backend classes, and defines the API they implement.
import os
import inspect
from interface import implements

from xtlib.console import console

from xtlib import utils
from xtlib import errors
from xtlib import scriptor
from xtlib import pc_utils
from xtlib import constants
from xtlib import file_utils

from .backend_interface import BackendInterface

class BackendBase(implements(BackendInterface)):

    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        self.compute = compute
        self.compute_def = compute_def
        self.blobfuse_index = 0
        self.is_windows = False
        self.fn_wrapped = None

    # API 
    def get_name(self):
        '''
        This method is called return the name of the backend service.
        '''
        pass

    # API 
    def adjust_run_commands(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, args):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  At the
        time this is called, files can still be added to snapshot_dir.
        '''
        pass

    # API 
    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
            repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):
        raise Exception("backend API function not implemented: submit_job")

    # API 
    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):
        raise Exception("backend API function not implemented: view_status")

    # API 
    def get_client_cs(self, service_node_info):
        raise Exception("backend API function not implemented: get_client_cs")
    
    # API 
    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        '''
        return False

    # API 
    def cancel_runs_by_names(self, workspace, run_names, box_name):
        '''
        Args:
            workspace: the name of the workspace containing the run_names
            run_names: a list of run names
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of cancel_result records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs")

    # API 
    def cancel_runs_by_job(self, job_id, runs_by_box):
        '''
        Args:
            job_id: the name of the job containing the run_names
            runs_by_box: a dict of box_name/run lists
        Returns:
            cancel_results_by box: a dict of box_name, cancel_result records
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs_by_job")

    # API 
    def cancel_runs_by_user(self, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs_by_user")

    # common code
    def append(self, cmds, cmd, echo_before=False, echo_after=False, expand=False):
        
        echo = "@echo" if self.is_windows else "echo"

        if expand:
            cmd = self.expand_system_names(cmd)

        if self.is_windows and not cmd.startswith("@"):
            cmd = "@" + cmd

        if echo_before:
            cmds.append("{} running: {}".format(echo, cmd))

        cmds.append(cmd)

        if echo_after:
            cmds.append("{} after: {}".format(echo, cmd))

    def get_activate_cmd(self):

        setup_def = self.config.get_setup_from_target_def(self.compute_def)

        if pc_utils.is_windows:
            activate_cmd = utils.safe_value(setup_def, "activate")
        else:
            # Attempting to activate the Conda shell from within a bash script
            # fails, with Conda saying that the bash environment has not
            # been correctly initialized to use Conda.
            # This thread https://stackoverflow.com/questions/34534513/calling-conda-source-activate-from-bash-script
            # eventually led me to the following command which is taken
            # from the lines of bash script that Conda appends to your
            # .bashrc file upon installation. This command is what
            # allows you to activate the Conda environment within a
            # bash shell. It returns a script generated by Conda
            # which is executed, and which stes up the conda
            # activate / deactivate commands in the encironment.
            conda_shell_bash_hook_cmd = 'eval "$(conda shell.bash hook)"'
            activate_cmd = utils.safe_value(setup_def, "activate")
            activate_cmd = "{} && {}".format(
                conda_shell_bash_hook_cmd, activate_cmd)

        return activate_cmd

    def get_service_name(self):
        if not "service" in self.compute_def:
            errors.config_error("missing 'service' property for xt config file compute target '{}'".format(self.compute))
        service_name = self.compute_def["service"]
        return service_name

    def object_to_dict(self, obj, columns):
       obj_dict = {col: getattr(obj, col) for col in columns if hasattr(obj, col)}
       return obj_dict
        
    def create_blobfuse_commands(self, storage_name, storage_key, sudo_available, mount_requests, install_blobfuse, 
            use_username=True, use_allow_other=True, nonempty=False):
        username = "$USER"
        cmds = []
        sudo = "sudo " if sudo_available else ""

        if install_blobfuse:
            # configure apt for microsoft products
            cmds.append("wget https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb")
            cmds.append("dpkg -i packages-microsoft-prod.deb")
            cmds.append("apt-get update")

            # install blobfuse
            # without specifying version, we get version 1.2.3 on AML which breaks our code
            version = "1.0.3"         
            cmds.append("{}apt-get install blobfuse={}".format(sudo, version))

        # for each mount request
        for md in mount_requests:
            mnt_dir = md["mnt_dir"]
            container_name = md["container"]
            readonly = md["readonly"]

            self.blobfuse_index += 1
            #tmp_dir = "/mnt/resource/blobfusetmp{}".format(self.blobfuse_index)
            tmp_dir = "$HOME/blobfusetmp{}".format(self.blobfuse_index)
            fn_config = "$HOME/fuse{}.cfg".format(self.blobfuse_index)
            readonly_opt = "-o ro" if readonly else ""
            nonempty_opt = "-o nonempty" if nonempty else ""

            sub_cmds = []
            sub_cmds.append("{}mkdir {} -p".format(sudo, mnt_dir))

            if use_username:
                sub_cmds.append("{}chown {} {}".format(sudo, username, mnt_dir))

            allow_other = "-o allow_other" if use_allow_other else ""

            sub_cmds += [
                "mkdir {} -p".format(tmp_dir),
                #"sudo chown {} {}".format(username, tmp_dir),

                # create fuse config file (clunky but it works)
                "echo accountName {} > {}".format(storage_name, fn_config),
                "echo accountKey {} >> {}".format(storage_key, fn_config),
                "echo containerName {} >> {}".format(container_name, fn_config),

                #"echo here is the config file '{}' contents".format(fn_config),
                #"more {}".format(fn_config),

                # keep it private 
                "chmod 600 {}".format(fn_config),
                "echo about to run blobfuse",
                "blobfuse -v",

                "{}blobfuse {} --tmp-path={}  --config-file={} {} -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 {} {}" \
                    .format(sudo, mnt_dir, tmp_dir, fn_config, readonly_opt, allow_other, nonempty_opt),

                "echo just ran blobfuse, here is ls -l on mnt_dir",
                "ls -l {}".format(mnt_dir),
            ]

            cmds += sub_cmds

        return cmds

    def create_download_commands(self, xt_path, create_dest_dirs, sudo_available, download_requests, 
            is_windows=False, use_username=True):
        cmds = []
        username = "$USER"
        #xt_path = "call " + xt_path if is_windows else xt_path
        sudo = "sudo " if (sudo_available and not is_windows) else ""

        # for each mount request
        for md in download_requests:
            container_name = md["container"]
            blob_path = md["blob_path"]
            dest_dir = md["dest_dir"]

            if create_dest_dirs:
                if is_windows:
                    # fix slashes for windows
                    dest_dir = dest_dir.replace("/", "\\")
                    sub_cmds = \
                    [ 
                        "mkdir {} ".format(dest_dir),
                    ]
                else:
                    sub_cmds = \
                    [ 
                        "{}mkdir {} -p".format(sudo, dest_dir),
                    ]
                    if use_username:
                        sub_cmds.append("{}chown {} {}".format(sudo, username, dest_dir))

                cmds += sub_cmds

            cmd = "{} download /{}/{} {}".format(xt_path, container_name, blob_path, dest_dir)
            self.append(cmds, cmd, True, True)

        return cmds        

    def emit_mount_cmds(self, cmds, storage_name, storage_key, container, store_path, mnt_path, is_writable, 
        install_blobfuse, sudo_available, use_username, use_allow_other, env_var_name, env_var_name2, 
        nonempty=False, cleanup_needed=False,):

        if self.is_windows:
            # TODO: provide pseudo-mount for local machine by using data-local and store-local config properties
            errors.combo_error("Mounting of Azure storage (for '{}') not supported by target OS (Windows)".format(store_data_dir))

        if cleanup_needed:
            # on pool machines, for any action, always UNMOUNT mnt_dir 
            # also, always zap the folder in case in was used in downloading files
            sudo = "sudo " if sudo_available else ""

            self.append(cmds,"{}fusermount -u -q {}".format(sudo, mnt_path))
            # do NOT call rm as it can delete cloud data if fusermount -u failed 
            #self.append(cmds,"{}rm -rf {}".format(sudo, mnt_path))

        # for now, all commands can assume linux form
        self.append(cmds, "echo MOUNTING {} to container {}".format(mnt_path, container))
        full_mnt_path = mnt_path + "/" + store_path
        self.append(cmds, "echo running export {}={}".format(env_var_name, full_mnt_path))

        self.append(cmds, 'echo setting {}="{}"'.format(env_var_name, full_mnt_path))

        self.append(cmds, 'export {}={}'.format(env_var_name, full_mnt_path))
        self.append(cmds, 'export {}={}'.format(env_var_name2, full_mnt_path))

        requests = [ {"container": container, "mnt_dir": mnt_path, "readonly": not is_writable} ]
        sub_cmds = self.create_blobfuse_commands(storage_name, storage_key, sudo_available, requests, install_blobfuse=install_blobfuse,
            use_username=use_username, use_allow_other=use_allow_other, nonempty=nonempty)
        cmds += sub_cmds

    def process_action(self, cmds, action, mnt_path, env_var_name, env_var_name2, container, store_data_dir, is_writable,
        storage_name, storage_key, sudo_available=True, cleanup_needed=False, is_windows=False, use_username=True, 
        install_blobfuse=False, use_allow_other=True, nonempty=False):

        self.is_windows = is_windows

        if action == "mount":
            self.emit_mount_cmds(cmds, storage_name, storage_key, container, store_path=store_data_dir, mnt_path=mnt_path, 
                is_writable=is_writable, install_blobfuse=install_blobfuse, sudo_available=sudo_available, 
                use_username=use_username, use_allow_other=use_allow_other, env_var_name=env_var_name, env_var_name2=env_var_name2, 
                nonempty=nonempty, cleanup_needed=cleanup_needed)

        elif action == "use_local":
            setter = "set" if is_windows else "export"
            self.append(cmds, "echo USING LOCAL path for ENV[{}]= {}".format(env_var_name, store_data_dir))
            self.append(cmds, '{} {}={}'.format(setter, env_var_name, store_data_dir))
            self.append(cmds, '{} {}={}'.format(setter, env_var_name2, store_data_dir))

        elif action == "download":
            # here, commands must be obey is_windows
            self.append(cmds, "echo DOWNLOADING {} from container {}".format(mnt_path, container))

            if is_windows:
                self.append(cmds, 'set {}={}'.format(env_var_name,  mnt_path))
            else:
                full_mnt_path =  mnt_path + "/" + store_data_dir
                self.append(cmds, 'export {}={}'.format(env_var_name,  full_mnt_path))

            self.append(cmds, "echo setting {}={}".format(env_var_name, store_data_dir))

            # make it look like this is parent dir
            dest_dir_ext = mnt_path + "/" + store_data_dir

            requests = [ {"container": container, "blob_path": store_data_dir, "dest_dir": dest_dir_ext} ]
            sub_cmds = self.create_download_commands("xt", True, sudo_available, requests, is_windows=is_windows, 
                use_username=use_username)
            cmds += sub_cmds

    def get_action_args(self, args):
        store_data_dir = args["data_share_path"]
        data_action = args["data_action"]
        data_writable = args["data_writable"]

        store_model_dir = args["model_share_path"]
        model_action = args["model_action"]
        model_writable = args["model_writable"]

        storage_name = args["storage"]
        storage_info = self.config.get("external-services", storage_name, default_value=None)
        if not storage_info:
            self.config_error("storage name '{}' not defined in [external-services] in config file".format(storage_name))

        # TODO: remove this reliance on specific storage providers 
        storage_key = storage_info["key"] if "key" in storage_info else None

        return store_data_dir, data_action, data_writable, store_model_dir, model_action, model_writable, storage_name, storage_key

    def add_xt_setup_cmds(self, cmds, is_windows):
        # add "." to PYTHONPATH so that any run of xt.exe will pick up latest XTLIB and USER LIBS
        if is_windows:
            cmd = "set PYTHONPATH=.;%PYTHONPATH%"
        else:
            cmd = "export PYTHONPATH=.:$PYTHONPATH"

        self.append(cmds, cmd)
        #self.append(cmds, "xt --version")

    def expand_system_names(self, cmd):

        if self.is_windows:
            cmd = cmd.replace("$call", "call")
            cmd = cmd.replace("$export", "set")
        else:
            cmd = cmd.replace("$call", "")
            cmd = cmd.replace("$export", "export")

        if "$current_conda_env" in cmd:
            conda = pc_utils.get_conda_env() 
            if conda:
                cmd = cmd.replace("$current_conda_env", conda)
        
        return cmd

    def add_first_cmds(self, cmds, script_name, change_dir):

        # don't add this as a cmd (breaks our script on philly)
        # if not pc_utils.is_windows():
        #     self.append(cmds, "#!/bin/sh")

        self.append(cmds, 'echo ----- START of XT-level processing -----')
        self.append(cmds, "echo running: " + script_name)

        self.append(cmds, 'echo initial cwd: {}'.format("%cd%" if self.is_windows else "$PWD"))
        cwd = utils.get_controller_cwd(self.is_windows, False)
        cwd = file_utils.fix_slashes(cwd, is_linux=not self.is_windows)

        if self.is_windows:
            self.append(cmds, 'echo 1st ARG, node_id= %1%')
            self.append(cmds, 'echo 2nd ARG, run_name= %2%')
            self.append(cmds, "mkdir {} 2>nul".format(cwd), echo_before=True)
        else:
            # echo commands as they are executed
            self.append(cmds, 'set -x')

            self.append(cmds, 'echo 1st ARG, node_id= $1')
            self.append(cmds, 'echo 2nd ARG, run_name= $2')
            self.append(cmds, "mkdir {} -p".format(cwd), echo_before=True)

        if change_dir:
            self.append(cmds, "cd {}".format(cwd), echo_before=True)
            self.append(cmds, 'echo after cd, cwd: {}'.format("%cd%" if self.is_windows else "$PWD"))

    def add_report_cmds(self, cmds, include_pytorch=False):
        if not self.is_windows:
            self.append(cmds, "echo '---------- MEMORY Report -----------:'")
            self.append(cmds, "free -mh")

            self.append(cmds, "echo '---------- CPU Report -----------:'")
            self.append(cmds, "lscpu")

        self.append(cmds, "echo '---------- GPU Report -----------:'")
        self.append(cmds, "nvidia-smi")

        self.append(cmds, "echo '---------- PYTHON Report -----------:'")
        self.append(cmds, 'python -V')
        #self.append(cmds, 'python3 -V')

        if include_pytorch:
            # temp debugging: we should not pull in a dependency on pytorch, but we know it is pre-installed on Philly
            self.append(cmds, "echo '---------- PYTORCH Report -----------:'")
            self.append(cmds, '''python -c "import torch; print('TORCH version', torch.__version__, ' says CUDA available=', torch.cuda.is_available())"''')

    def wrap_user_command(self, user_parts, snapshot_dir, store_data_dir, data_action, data_writable, \
        store_model_dir, model_action, model_writable, storage_name, storage_key, actions, is_windows, 
        sudo_available=True, username=None, use_username=True, install_blobfuse=False, pip_freeze=True, 
        setup=None, post_setup_cmds=None, args=None, nonempty=False, change_dir=True, use_allow_other=True):

        '''
        we need to run several commands to configure the target machine for our run, and then run the user's commands (user_parts).
        we do this by writing all the commands (config cmds and user_parts) to shell script or batch file that resides in the 
        "snapsnot_dir".  all files in the snapshot_dir will be zipped and uploaded to the job store at job submit time, and then
        downloaded and unzipped on the target machine at run launch time.
        '''
        self.is_windows = is_windows
        script_name = constants.FN_WRAPPED_BAT if is_windows else constants.FN_WRAPPED_SH
        cmds = []

        self.add_first_cmds(cmds, script_name, change_dir=change_dir)
        self.add_setup_cmds(cmds, pip_freeze, args)
        self.add_xt_setup_cmds(cmds, is_windows)
        self.add_report_cmds(cmds)

        if username:
            self.append(cmds, "$export USER=" + username, expand=True)

        self.append(cmds, "echo -------------- Data ACTIONS -------------")

        # put mnt paths in user's home dir so sudo isn't needed to create/mount
        data_mount_dir = "%USERPROFILE%\\mnt\\data" if is_windows else "~/mnt_data"
        model_mount_dir = "%USERPROFILE%\\mnt\\models" if is_windows else "~/mnt_models"

        # emit cmds to MOUNT run store OUTPUT path
        if not self.is_windows:
            workspace = args["workspace"]
            store_path = "runs/$2/output"   # uses RUN_NAME arg (passed to script)

            self.emit_mount_cmds(cmds, storage_name, storage_key, container=workspace, store_path=store_path, 
                mnt_path="$HOME/mnt/workspace", is_writable=True, install_blobfuse=install_blobfuse, 
                sudo_available=sudo_available, use_username=use_username, use_allow_other=use_allow_other, env_var_name="XT_OUTPUT_DIR", 
                env_var_name2="XT_OUTPUT_MNT", nonempty=nonempty, cleanup_needed=True)

        # emit cmds to MOUNT or DOWNLOAD data
        if "data" in actions:
            self.process_action(cmds, data_action, data_mount_dir, "XT_DATA_DIR", "XT_DATA_MNT", utils.DATA_STORE_ROOT, 
                store_data_dir, data_writable, storage_name, storage_key, sudo_available=sudo_available, cleanup_needed=True, 
                is_windows=is_windows, use_username=use_username, install_blobfuse=install_blobfuse, nonempty=nonempty,
                use_allow_other=use_allow_other)

        # emit cmds to MOUNT or DOWNLOAD model
        if "model" in actions:
            self.process_action(cmds, model_action, model_mount_dir, "XT_MODEL_DIR", "XT_MODEL_MNT", utils.MODELS_STORE_ROOT, 
                store_model_dir, model_writable, storage_name, storage_key, sudo_available=sudo_available, cleanup_needed=True, 
                is_windows=is_windows, use_username=use_username, install_blobfuse=install_blobfuse, nonempty=nonempty,
                use_allow_other=use_allow_other)

        if pip_freeze:
            self.append(cmds, "echo final PIP FREEZE:")
            self.append(cmds, "pip freeze > __final_pip_freeze__.log")

        # add post setup commands now
        if post_setup_cmds:
            cmds += post_setup_cmds

        if self.is_windows:
            self.append(cmds, '@set XT_NODE_ID=%1%')
            self.append(cmds, "echo XT_NODE_ID=%XT_NODE_ID%")
        else:
            self.append(cmds, 'export XT_NODE_ID=$1')
            self.append(cmds, "echo XT_NODE_ID=$XT_NODE_ID")

        # TODO: remove special experiment here so that direct-mode will work
        hardcode_controller = False    

        if hardcode_controller:
            # experiment
            user_cmd = self.get_controller_run_cmd()
            self.append(cmds, "echo running controller with: {}".format(user_cmd))
            self.append(cmds, user_cmd)
        else:
            # run user's cmd
            user_cmd = " ".join(user_parts)
            
            # append the "put args from containing batch/sh file here" marker
            args_here = " %*" if is_windows else " $*"  
            user_cmd += args_here
            self.append(cmds, user_cmd)
        
        # remove empty cmds
        cmds = [cmd for cmd in cmds if cmd]

        # for more reliable and easier-to-debug operation, write cmds to a .sh/.bat file (in snapshot_dir)
        if is_windows:
            fn_wrapped = snapshot_dir + "/" + constants.FN_WRAPPED_BAT
            scriptor.write_script_file(cmds, fn_wrapped, is_windows)
        else:
            fn_wrapped = snapshot_dir + "/" + constants.FN_WRAPPED_SH
            scriptor.write_script_file(cmds, fn_wrapped, is_windows)

        # copy to submit-logs
        utils.copy_to_submit_logs(args, fn_wrapped)

        # remember where we wrote the wrapped file
        self.fn_wrapped = fn_wrapped

        return fn_wrapped

    def get_controller_run_cmd(self, external_controller_port=constants.CONTROLLER_PORT, is_aml=False):

        if self.is_windows:
            text = '''python -u -c "from xtlib.controller import run; run(port={}, is_aml={})" '''
        else:
            # linux needs these escapes around the double quotes
            text = '''python -u -c 'from xtlib.controller import run; run(port={}, is_aml={})'  '''

        cmd = text.format(external_controller_port, is_aml)
        return cmd

    def add_pip_packages(self, cmds, pip_packages):
        if pip_packages:
            cmd = "pip install" if self.is_windows else "pip install --user"
            # NOTE: double quotes around package names cause error on linux
            for pp in pip_packages:
                cmd += ' {}'.format(pp)

            cmd += " > __pip_install__.log"
            self.append(cmds, cmd, True, True)

    def add_conda_packages(self, cmds, conda_packages):
        if conda_packages:
            cmd = "conda install"
            # NOTE: double quotes around package names cause error on linux
            for cp in conda_packages:
                cmd += ' {}'.format(cp)

            cmd += " > __conda_install__.log"
            self.append(cmds, cmd, True, True)

    def add_setup_cmds(self, cmds, pip_freeze, args):

        activate_cmd = self.get_activate_cmd()
        if activate_cmd:
            if self.is_windows and not activate_cmd.startswith("call") and not activate_cmd.startswith("@call"):
                activate_cmd = "@call " + activate_cmd                
            self.append(cmds, activate_cmd, expand=True)

        if self.is_windows:
            self.append(cmds, "echo CONDA: %CONDA_DEFAULT_ENV%")
        else:
            self.append(cmds, "echo CONDA: $CONDA_DEFAULT_ENV")

        if pip_freeze:
            self.append(cmds, "echo initial PIP FREEZE:")
            self.append(cmds, "pip freeze > __initial_pip_freeze__.log")

        # install CONDA-PACKAGES
        conda_packages = args["conda_packages"]
        if conda_packages:
            self.add_conda_packages(cmds, conda_packages)

        # install PIP-PACKAGES (xtlib and user-specified others)
        pip_packages = args["pip_packages"]
        if pip_packages:
            self.add_pip_packages(cmds, pip_packages)

        # we use pip install --local, so add it to the path
        if self.is_windows:
            self.append(cmds, '@set PATH=%HOME%/.local/bin;%PATH%')
        else:
            self.append(cmds, 'export PATH=$HOME/.local/bin:$PATH')

    # API call
    def get_node_status(self, service_node_info):
        pass

    # API call
    def read_log_file(self, service_node_info, log_name, start_offset=0, end_offset=None, 
        encoding='utf-8', use_best_log=True):
        pass

    # API call
    def get_simple_status(self, status):
        # translates an Philly status to a simple status (queued, running, completed)
        pass

    # API call
    def cancel_job(self, service_job_info, service_info_by_node):
        pass
    
    # API call
    def cancel_node(self, service_node_info):            
        pass

    # API call
    def get_service_queue_entries(self, service_node_info):
        pass