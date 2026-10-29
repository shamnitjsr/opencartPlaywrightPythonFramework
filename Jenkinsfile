pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run on')
        string(name: 'MARKERS', defaultValue: 'sanity or regression', description: 'Pytest marker expression')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shamnitjsr/opencartPlaywrightPythonFramework.git'
                    // credentialsId: 'github-creds'   // uncomment for a private repo
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                "C:\\Users\\SHAMBHU KUMAR\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m venv .venv
                .venv\\Scripts\\python.exe -m pip install --upgrade pip
                .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                .venv\\Scripts\\python.exe -m playwright install ${params.BROWSER}
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                .venv\\Scripts\\python.exe -m pytest tests -m "${params.MARKERS}" --browser=${params.BROWSER} --junitxml=reports/junit.xml
                """
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true

            // Uncomment ONLY after installing the Allure Jenkins plugin
            // and adding an "allure" tool under Manage Jenkins -> Tools
            // allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]

            // Uncomment ONLY after installing the HTML Publisher plugin
            // publishHTML(target: [
            //     reportDir: 'reports',
            //     reportFiles: 'myreport.html',
            //     reportName: 'Pytest HTML Report',
            //     keepAll: true,
            //     allowMissing: true,
            //     alwaysLinkToLastBuild: true
            // ])
        }
    }
}