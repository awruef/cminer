# CMiner

Overall flow:
 * Identify a project to mine, by URL
 * Clone that project into the workspace directory
 * Build that project in place in the workspace directory, generating a 
   `compile_commands.json`
 * Run the query tool on each compilation unit in `compile_commands.json`,
   storing the results in a database

Persistent information:
 * Queries to run 
 * Results from each query 
 * Projects that have been built and are ready for query
 * A queue of projects to mine

Tools we need:
 * Builder
 * Wrapper around query tool
 * Coordination infrastructure
   + A database schema to keep the persistent information
   + A tool to add to the queue of projects to mine
   + A Mesos framework to manage the overall flow 
   + A few Mesos agents that deal with the builder and query
