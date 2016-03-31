#!/usr/bin/python


def kubernetes(module, conf_path):
    kubectl_path = module.get_bin_path('kubectl', required=True)
    args = [kubectl_path, "create", "-f", conf_path]
    (rc, stdout, stderr) = module.run_command(args)
    return rc == 0


def main():
    module = AnsibleModule(
        argument_spec=dict(
            k8s_config_path=dict(required=True)
        )
    )

    k8s_artifacts = module.params['k8s_config_path']

    if kubernetes(module, k8s_artifacts):
        module.exit_json(changed=False)


from ansible.module_utils.basic import *

main()