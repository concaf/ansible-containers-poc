Vagrant.configure(2) do |config|

DOCKER_REGISTRY="docker.io"
IMAGE_NAME="openshift/origin"
IMAGE_TAG="v1.1.1"
PUBLIC_ADDRESS="10.1.2.2"
PUBLIC_HOST="adb.cluster.io"

    config.vm.provider "libvirt" do |libvirt, override|
      libvirt.driver = "kvm"
      libvirt.memory = 2048
      libvirt.cpus = 2
    end

# docker is here
    config.vm.define "docker" do |docker|
        docker.vm.box = "fedora/23-cloud-base"
        docker.vm.hostname = "docker"
        docker.vm.network "private_network", ip: "192.168.33.10"
	docker.vm.provision "shell", inline: <<-SHELL
          echo vagrant | sudo passwd root --stdin
	  sudo dnf update -y
	  sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/fedora/$releasever/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
	  sudo dnf install docker-engine -y
	  sudo systemctl enable docker
	  sudo systemctl restart docker
	  if [ ! -f /usr/local/bin/docker-compose ]; then
sudo su -c "curl -L https://github.com/docker/compose/releases/download/1.6.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose"
fi
	  sudo chmod +x /usr/local/bin/docker-compose
	  sudo su -c "echo export PATH=/usr/local/bin:$PATH >> ~/.bashrc"

	SHELL
    end


# kubernetes is here
    config.vm.define "kubernetes" do |kubernetes|
        kubernetes.vm.box = "projectatomic/adb"
        kubernetes.vm.hostname = "kubernetes"
        kubernetes.vm.network "private_network", ip: "192.168.33.20"
	  kubernetes.vm.provision "shell", inline: <<-SHELL
	    echo vagrant | sudo passwd root --stdin
	    sudo mkdir -p /etc/pki/kube-apiserver/
	    sudo openssl genrsa -out /etc/pki/kube-apiserver/serviceaccount.key 2048
	    sudo sed -i.back '/KUBE_API_ARGS=*/c\KUBE_API_ARGS="--service_account_key_file=/etc/pki/kube-apiserver/serviceaccount.key"' /etc/kubernetes/apiserver
	    sudo sed -i.back '/KUBE_CONTROLLER_MANAGER_ARGS=*/c\KUBE_CONTROLLER_MANAGER_ARGS="--service_account_private_key_file=/etc/pki/kube-apiserver/serviceaccount.key"' /etc/kubernetes/controller-manager

	    echo "setup master"
	    for service in etcd kube-apiserver kube-controller-manager kube-scheduler; do
	      echo "  enable $service"
	      sudo systemctl enable $service

	      echo "  start $service"
	      sudo systemctl start $service
	    done

	    echo "setup nodes"
	    for service in kube-proxy kubelet; do
	      echo "  enable $service"
	      sudo systemctl enable $service

	      echo "  start $service"
	      sudo systemctl start $service
	    done
	    echo "  restart docker"
	    sudo systemctl restart docker
	  SHELL
	end


# openshift is here

    config.vm.define "openshift" do |openshift|
        openshift.vm.box = "projectatomic/adb"
        openshift.vm.hostname = "openshift"
        openshift.vm.network "private_network", ip: "192.168.33.30"

  openshift.vm.provision "shell", inline: <<-SHELL
    echo vagrant | sudo passwd root --stdin
    sudo DOCKER_REGISTRY=#{DOCKER_REGISTRY} IMAGE_TAG=#{IMAGE_TAG} IMAGE_NAME=#{IMAGE_NAME} /usr/bin/sccli openshift
    echo "You can now access OpenShift console on: https://#{PUBLIC_ADDRESS}:8443/console"
    echo
    echo "Configured basic user: openshift-dev, Password: devel"
    echo
    echo "Configured cluster admin user: admin, Password: admin"
    echo
    echo "To use OpenShift CLI, run:"
    echo "$ vagrant ssh"
    echo "$ oc login"
    echo
    echo "To browse the OpenShift API documentation, follow this link:"
    echo "http://openshift3swagger-claytondev.rhcloud.com"
    echo
    echo "Then enter this URL:"
    echo https://#{PUBLIC_ADDRESS}:8443/swaggerapi/oapi/v1
    echo "."
    sudo oc login localhost:8443 --username=admin --password=admin --insecure-skip-tls-verify=true
  SHELL
end

end
