Dear Madeleine,

Thank you very much for your email and for giving me the opportunity to respond to these questions in writing. Please find my answers below:

1. Can you please talk about your experience with Unreal Engine or any other game engines?
- Between 2011 and 2013, while working at Kingsoft, I used Unreal Engine 2 to contribute to the following games:
	- RushTeam (FPS Online) – Animation Lead
	- Mission Against Terror (FPS Online) – Animation Lead
	- Legend of Shengdao (3D Wuxia RPG) – Lead Animator, responsible for model and animation engine integration
	- Fox Three Kingdoms (3D Fantasy RPG) – Animation Lead during initial launch

- during my time at Snail Games and Seven Senses Game, I worked on three UE4-based games:
	- ARK Park (VR, UE4)_ – Animator (2016–2018) [Steam Page](https://store.steampowered.com/app/529910/ARK_Park/)
	- ZCrew (PC, UE4)_ – Sole animator in early development (2018–2019) [Steam Page](https://store.steampowered.com/app/1386650/ZcrewZ/)
	- Myth of Empires (UE4)_ – Animation Supervisor (2019–2024); led all rigging and animation efforts for this large-scale sandbox game [Steam Page](https://store.steampowered.com/app/1371580/_/)

- Currently, at Seven Senses, I’m leading the animation and rigging effort for an **unnamed sandbox project** built with **UE5**, which is still in development.

I’ve been using UE4 and UE5 extensively, focusing on rigging, animation systems design, asset integration, and animation pipeline development. I work with Control Rig, cloth simulation, physical assets, and  familiar with Blueprint, Animation Blueprints, and state machines. I also have a working knowledge of ALSv4.

2. Are you comfortable and experienced using Maya and/or Control Rig? 
I am highly proficient in Maya, with deep experience in rigging, animation, and Python scripting. I am capable of both manual rigging and using modular systems like mGear and Advanced Skeleton, and have written many scripts to automate and improve animation workflows.

In Unreal Engine, I am comfortable with Control Rig. We often purchase monster animation assets from the Marketplace(Fab), which don’t include rig files. Control Rig has proven essential for editing and creating new animations directly in-engine.

I also use Control Rig for procedural animations, corrective poses, and secondary motion like breasts or hair. For breast jiggle, I typically use physical assets with RigidBody node. For ponytail dynamics, we often use the Kawaii Physics plugin.

3. Please share your experience with rigging? What kind of things have you rigged? And what is your process?
I’ve rigged a wide variety of characters including realistic and stylized bipeds, quadrupeds, many types of creatures and monsters, facial rigs, weapons, and props.

Here’s my typical rigging process:
- Model check & preparation
- Skeleton design & setup(Correct Joint Orientation and Rotate Order)
- Rig system setup
	- Create Controls, 
		- including a dedicated root joint controller, to make it easier for animators to create root motion animation.
    - IK/FK systems with switching
    - Space switching
    - Limb scaling and volume preservation
    - Detailed finger and foot rigging
    - Clothing and weapon rigging, with weapon space switching 
	    - implemented to allow the weapon to switch between left hand, right hand, pelvis, spine and world space.
- Skinning(Using ngSkinTools) & deformation testing
- Facial rigging(bone-based, blendshape-based, or hybrid)
- UI control setup & automation scripting
For efficiency, we often use mGear or Advanced Skeleton. I personally prefer mGear for its flexibility and robustness.

4. How do you stay organized and ahead in a fast-paced production environment? Can you share any specific strategies or tools you use?
Here are my main strategies:
- Enforce naming conventions and use version control (SVN / Git)
- Adopt a Data Centric Rigging Structure – separating model assets, skinning data, blenshape data, scripts data and rig data for easier management
- Develop custom tools for batch processing animation and rigging data
- Automate repetitive tasks with Python scripts to reduce human error
- Maintain close communication with animators, programmers, and designers to stay aligned
- Write clear documentation to ensure teammates can understand and use tools efficiently

5. What is your current notice period, and when would you be available to start if offered the position?  
My current notice period is **one month**, but I am open to coordinating an earlier handover if necessary.

6. What motivates you to join Epic Games?
Epic Games represents the cutting edge of real-time technology and creative tooling. I have always been passionate about animation and technology, and Epic's ongoing innovation in tools and engine development inspires me.

Joining Epic would allow me to learn from and collaborate with world-class developers, and to contribute to impactful projects — an ideal next step in my career.

7. This role is studio-based. Are you comfortable working full-time at our Shanghai studio?
Yes, I am fully open and committed to working full-time on-site at the Shanghai studio. I look forward to collaborating in person with the team.

8. What are your salary expectations for this role?
My expected salary is **RMB 500,000 per year (pre-tax)**. Of course, I’m open to further discussion based on the role’s responsibilities and the company’s benefits.

9. Is there anything else about your experience that you would like to share? 
I have over 15 years of experience in animation and rigging, working on FPS, MMORPG, MOBA, VR, and sandbox games. I’ve often been the only tech animator on a team, bridging the gap between artists and engineers.

I specialize in problem-solving, system building, and tool development, and am also passionate about workflow optimization and training. I believe I can bring immediate value to the team while continuing to grow.

Please feel free to reach out if you have any additional questions or would like to schedule a follow-up call.

Best regards,  
**Charles Tian (田超)**  