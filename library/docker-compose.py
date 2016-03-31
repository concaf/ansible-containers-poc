#!/usr/bin/python


def docker(module, conf_path):
    docker_compose_path = module.get_bin_path('docker-compose', required=True)
    args = [docker_compose_path, "-f", conf_path, "up", "-d"]
    (rc, stdout, stderr) = module.run_command(args)
    return rc == 0


def main():
    module = AnsibleModule(
        argument_spec=dict(
            docker_compose_config_path=dict(required=True)
        )
    )

    docker_compose_artifacts = module.params['docker_compose_config_path']+"/docker-compose.yml"

    if docker(module, docker_compose_artifacts):
        module.exit_json(changed=False)


from ansible.module_utils.basic import *

main()