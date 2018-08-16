# lrose-test
automatic integration, build and test of lrose code



```
pipeline {
  
    agent {
        //docker { image 'nsflrose/lrose-blaze:latest' }
        //docker { image 'centos-source:Dockerfile' }
        docker { image 'centos-jenkins-base:latest' }
    }
    
    environment {
        LD_LIBRARY_PATH = '/usr/local/lrose/lib'
        // setting the PATH doesn't seem to work 
        PATH = "/usr/local/lrose/bin:$PATH"  
    }
    
    stages {
        stage('Fetch and Build') {
            steps {
                sh 'cd /tmp/bj; tar xvfz lrose-blaze-20180516.src.tgz'

                // The distribution will be unpacked into a subdirectory:

                sh '/tmp/bj/lrose-blaze-20180516.src/build/checkout_and_build_auto.py --package lrose-blaze --prefix /usr/local/lrose --clean'
                //sh '/tmp/bj/lrose-blaze-20180516.src/build/checkout_and_build_auto.py --package lrose-blaze --clean'
            }
        }
        
        stage('Test') {
            steps {
                sh 'ls -lrt /usr/local/lrose/bin'
                sh 'ls -lrt /usr/local/lrose/lib'
                sh '/usr/local/lrose/bin/RadxPrint -h'
            }
        }
        
        stage('Test2') {
            steps {
                sh '/usr/local/lrose/bin/RadxConvert -h'
            }
        }
    }
}

```
