def branch 
def increment
def release=false

pipeline
{
    agent any
    
    tools
    {
        jdk "JDK8"
        maven "maven"
    }//tools

    environment 
    {
        JIRA_URL = 'http://jira:8080'
        J_USER = 'jira-root'
    }
    triggers 
    {
        gitlab(triggerOnPush: true, branchFilterType: 'All')
    }//triggers
    post 
    {
      failure 
      {
        echo '*****notify: FAILED!*****'
        updateGitlabCommitStatus name: 'build', state: 'failed'
      }
      success 
      {
        echo '*****notify: SUCCESS!*****'
        updateGitlabCommitStatus name: 'build', state: 'success'
      }
      always 
      {
        echo '**cleaning directory**'
        sh 'rm -rf'
        
        // emailext body: '$DEFAULT_CONTENT' , subject: '$DEFAULT_SUBJECT', to: '$DEFAULT_RECIPIENTS' 
      }
    }//post

    options
    {
       gitLabConnection('gitlab')
       timestamps() 
    }//options

    stages
    {
        stage("initialization")
        { //get versions.. check if branch is buildable
            steps
            {
                script
                {
                    dir("${env.WORKSPACE}"){

                    branch=BRANCH_NAME
                    sh 'git fetch --tags'
                    def found=false

                    if (branch.contains("release/")){
                        release=true
                        found=true
                        echo "runnig on branch: "+branch 
                        havetag_exitstatus=sh(script: 'git describe --exact-match --tags HEAD',returnStatus: true)
                        havetag=(havetag_exitstatus!=0) 
                        increment = sh(script: "bash ci/fetchTags.sh ${branch} ${havetag}",returnStdout: true)
                        echo "increment in groovy is "+increment

                    }

                    if (branch.equals("master")){
                        release=true
                        found=true
                        increment="master."+GIT_COMMIT.substring(0,5)
                    }

                    if (branch ==~"^([A-Z]+)-([0-9]+).*"){ //check for issue branch name pattern
                        found=true
                        //update Jira issue to "on progress"
                        withCredentials([usernameColonPassword(credentialsId: 'jira-root', variable: 'USERPASS')]) {
                            sh '''
                            set -e
                            ci/jira_comment.sh -U $JIRA_URL -h $GIT_COMMIT -i $GIT_BRANCH -u $USERPASS
                            ci/jira_status.sh -U $JIRA_URL -c "start" -i $GIT_BRANCH -u $USERPASS
                            '''
                        }
                    }
                    if (!found){ //exit pipeline
                        currentBuild.result = 'ABORTED'
                        error('branch is not supported')
                    }
                    }//dir
                }//script
            }//steps  
        }//initialization

        stage("build")
        {
            steps{
                script{
                    withMaven(maven: 'maven'){
                        if (branch ==~ "JIR-[0-9]*"){
                            sh 'mvn install -DskipTests'
                        } else {
                            sh "mvn versions:set -DnewVersion=${increment}"
                            sh "mvn install -DskipTests "
                        }
                    }//withMaven
                }//script
            }//steps
        }//build
        stage("test")
        {
            steps{
                echo 'test stage'
            } //steps
        }//test
        stage("tag")
        {
            steps{
                script{
                    if (release){
                        echo 'tagging git'
                        sh """
                        git reset --hard
                        git tag ${increment}
                        git push --tags
                        """ 
                    }
                }//script
            }//steps
        }//tag
    }//stages
}//pipeline


