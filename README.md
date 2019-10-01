# Xpilot-AI

This is my year long senior research project to test the viability of controlling an Xpilot agent with a neural net (see Sem 2 Research Presentation for more details)

THIS CAN ONLY BE RUN ON LINUX, follow Setup_Instructions.txt for installation instructions

Refresh_Weights.py creates/refreshes a nested list that is the weights of the neural net, it needs to be run first

Teach_Agent.py is the main meat of the project, in it there is a rules based agent that will just drive around an environment. While it is doing so its driving decisions and positional data are being fed to the neural net which is taught through backpropagation to copy this rules based agent. With the server running at 32 fps running this for about 30 minutes to let the net train should be sufficient.

Test_Learned_Agent.py is the script that reads the hopefully trained weights file and allows it to pilot its own agent.

Starting the server with: 
./xpilots -map maps/simple.xp -noQuit -switchBase 1 -fps 32 -map maps/lifeless.xp
is what I found to be the best training environment for Teach_Agent and Test_Learned_Agent

For more information on the technology:  http://xpilot-ai.org/
