# 
# vagrantfile for crawler
#

# very simple box

# config options
ip = '192.168.0.53'
hostname = 'crawler'
ram = '256'

# provision script
$script = <<SCRIPT
echo 'installing tweepy'
cd /tmp
git clone https://github.com/tweepy/tweepy.git
cd tweepy
sudo python setup.py install
cd /tmp
rm -rf tweepy
SCRIPT


Vagrant::Config.run do |config|
    config.vm.box = 'precise32'
    config.vm.box_url = 'http://files.vagrantup.com/precise32.box'
    config.vm.host_name = 'crawler'
    config.vm.network :hostonly, ip
    
    config.vm.customize [
        'modifyvm', :id,
        '--name', hostname,
        '--memory', ram
    ]
    
    config.vm.provision :shell, :inline => $script
end