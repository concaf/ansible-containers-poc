#!/usr/bin/python


def openshift(module, conf_path):
    oc_path = module.get_bin_path('oc', required=True)
    args = [oc_path, "create", "-f", conf_path]
    (rc, stdout, stderr) = module.run_command(args)
    return rc == 0


def main():
    module = AnsibleModule(
        argument_spec=dict(
            oc_config_path=dict(required=True)
        )
    )

    oc_artifacts = module.params['oc_config_path']

    if openshift(module, oc_artifacts):
        module.exit_json(changed=False)


from ansible.module_utils.basic import *

main()