# jiraci

This is a project that include a docker-compose of Jenkins, JIRA and gitlab.

# project goal

The goal is to create a CI/CD tool that integrate JIRA and gitlab in the following way:

1. For every new issue, the person who got assigned create a branch that start with the name of the issue. for example: JIR-1-something-to-add.
2. After he commit, the jenkins got trigger to start the proccess of the CI and changing the status in JIRA from "To Do" to "In Progress".
3. When the programmer has done working on his problem he is sending a merge-request (Notice that we only accept ff-only). If the build got successfull, jenkins update the status to "Done" and assign the issue number to the release version.