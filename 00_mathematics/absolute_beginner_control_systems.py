"""
Control Systems - Starting from ABSOLUTE BASICS
==============================================

Don't worry if control systems seems confusing! 
Let's start with simple everyday examples you already understand.

Think of these familiar situations:
- Driving a car and staying in your lane
- Taking a shower and adjusting water temperature  
- Using cruise control on a highway
- Thermostat controlling room temperature

These are ALL control systems! Let's learn step by step.
"""

import numpy as np
import matplotlib.pyplot as plt

def explain_basic_concept():
    """Start with the simplest possible explanation"""
    
    print("🌟 WHAT IS A CONTROL SYSTEM? (In Simple Words)")
    print("=" * 55)
    print()
    print("A control system is just a way to:")
    print("1. MEASURE what's happening (sensor)")
    print("2. COMPARE it to what you want (your brain)")
    print("3. ADJUST something to get what you want (your hands)")
    print()
    print("🚗 DRIVING EXAMPLE:")
    print("   - MEASURE: Your eyes see the car drifting right")
    print("   - COMPARE: Brain says 'I want to go straight'")  
    print("   - ADJUST: Your hands turn the steering wheel left")
    print()
    print("🚿 SHOWER EXAMPLE:")
    print("   - MEASURE: Your skin feels the water is too hot")
    print("   - COMPARE: Brain says 'I want comfortable temperature'")
    print("   - ADJUST: Your hand turns the cold water tap")
    print()
    print("That's it! Control systems are everywhere!")
    print("=" * 55)

def simple_water_tank_example():
    """Use a water tank - very easy to visualize"""
    
    print("\n🪣 LET'S START WITH A WATER TANK")
    print("=" * 40)
    print()
    print("Imagine a water tank with:")
    print("• A pipe filling it (water coming IN)")
    print("• A drain at the bottom (water going OUT)")
    print("• You want to keep the water level at 5 feet")
    print()
    
    # Simple simulation
    time = np.arange(0, 20, 0.1)  # 20 seconds
    
    # Starting conditions
    desired_level = 5.0  # We want 5 feet
    current_level = np.zeros(len(time))
    current_level[0] = 2.0  # Start with 2 feet of water
    
    valve_opening = np.zeros(len(time))  # How much we open the input valve
    
    # Manual control (like you controlling it)
    for i in range(1, len(time)):
        # Check current water level
        level_now = current_level[i-1]
        
        # Compare with what we want
        error = desired_level - level_now  # How far off are we?
        
        # Decide how much to open the valve
        if error > 0:  # Too low - need more water
            valve_opening[i] = min(1.0, error * 0.3)  # Open valve proportionally
        else:  # Too high - close valve
            valve_opening[i] = 0
        
        # Calculate water flow
        water_in = valve_opening[i] * 2.0  # Max 2 feet/sec input
        water_out = 0.5  # Constant drain of 0.5 feet/sec
        net_flow = water_in - water_out
        
        # Update water level
        dt = time[1] - time[0]
        current_level[i] = current_level[i-1] + net_flow * dt
    
    # Plot the results
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(time, current_level, 'b-', linewidth=3, label='Actual Water Level')
    plt.axhline(y=desired_level, color='r', linestyle='--', linewidth=2, label='Desired Level (5 ft)')
    plt.title('Water Tank Level Control', fontsize=14)
    plt.ylabel('Water Level (feet)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(time, valve_opening, 'g-', linewidth=2, label='Valve Opening')
    plt.title('Your Control Action', fontsize=14)
    plt.ylabel('Valve Opening (0=closed, 1=fully open)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    error = desired_level - current_level
    plt.plot(time, error, 'r-', linewidth=2, label='Error (Desired - Actual)')
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.title('Error: How Far Off We Are', fontsize=14)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Error (feet)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\n📊 WHAT YOU'RE SEEING:")
    print("• Blue line: Water level starts low, then rises to 5 feet")
    print("• Red dashed line: This is our TARGET (5 feet)")
    print("• Green line: How much we open the valve (our control)")
    print("• Red line: The ERROR (how far off we are)")
    print()
    print("🎯 KEY INSIGHT:")
    print("When ERROR is big → We take BIG action (open valve more)")
    print("When ERROR is small → We take SMALL action")
    print("When ERROR is zero → We're perfect! No action needed")

def explain_step_response_simply():
    """Explain step response with simple analogy"""
    
    print("\n\n🚶 WHAT IS A 'STEP RESPONSE'?")
    print("=" * 40)
    print()
    print("Think of it like this:")
    print("🔹 You're walking normally")
    print("🔹 Suddenly you decide to walk FASTER")
    print("🔹 How long does it take you to reach the new speed?")
    print("🔹 Do you instantly jump to the new speed? NO!")
    print("🔹 Do you gradually speed up? YES!")
    print()
    print("That's a STEP RESPONSE!")
    print("• STEP = Sudden change in what you want")
    print("• RESPONSE = How the system reacts to that change")
    print()
    
    # Simple step response example
    time = np.linspace(0, 5, 100)
    
    # Different types of responses
    plt.figure(figsize=(14, 10))
    
    # 1. Instant response (impossible in real life)
    plt.subplot(2, 3, 1)
    instant = np.zeros_like(time)
    instant[time >= 1] = 1
    plt.plot(time, instant, 'r-', linewidth=3)
    plt.title('Impossible: Instant Response', fontsize=12)
    plt.ylabel('Speed')
    plt.grid(True)
    plt.text(2.5, 0.5, "This can't happen\nin real life!", 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='yellow'))
    
    # 2. Fast response
    plt.subplot(2, 3, 2)
    fast = np.zeros_like(time)
    fast[time >= 1] = 1 - np.exp(-5*(time[time >= 1] - 1))
    plt.plot(time, fast, 'g-', linewidth=3)
    plt.title('Fast Response', fontsize=12)
    plt.ylabel('Speed')
    plt.grid(True)
    plt.text(2.5, 0.5, "Quick to reach\nnew speed", 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='lightgreen'))
    
    # 3. Slow response
    plt.subplot(2, 3, 3)
    slow = np.zeros_like(time)
    slow[time >= 1] = 1 - np.exp(-1*(time[time >= 1] - 1))
    plt.plot(time, slow, 'b-', linewidth=3)
    plt.title('Slow Response', fontsize=12)
    plt.ylabel('Speed')
    plt.grid(True)
    plt.text(2.5, 0.5, "Takes time to\nreach new speed", 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='lightblue'))
    
    # 4. Overshoot response
    plt.subplot(2, 3, 4)
    overshoot_time = time[time >= 1] - 1
    overshoot = np.zeros_like(time)
    overshoot[time >= 1] = 1 - np.exp(-3*overshoot_time) * np.cos(6*overshoot_time)
    plt.plot(time, overshoot, 'purple', linewidth=3)
    plt.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    plt.title('Overshoot Response', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.grid(True)
    plt.text(2.5, 0.5, "Goes too fast first,\nthen settles down", 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='plum'))
    
    # 5. Real car example
    plt.subplot(2, 3, 5)
    car_response = np.zeros_like(time)
    car_time = time[time >= 1] - 1
    car_response[time >= 1] = 1 - np.exp(-2*car_time)
    plt.plot(time, car_response, 'orange', linewidth=3)
    plt.title('Real Car Acceleration', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.grid(True)
    plt.text(2.5, 0.5, "Like pressing\ngas pedal", 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='orange', alpha=0.7))
    
    # 6. What we measure
    plt.subplot(2, 3, 6)
    plt.plot(time, car_response, 'orange', linewidth=3)
    plt.axhline(y=1, color='k', linestyle='--', alpha=0.7, label='Target Speed')
    plt.axhline(y=0.63, color='r', linestyle=':', label='63% of target')
    
    # Mark important points
    idx_63 = np.where(car_response >= 0.63)[0]
    if len(idx_63) > 0:
        t_63 = time[idx_63[0]]
        plt.axvline(x=t_63, color='r', linestyle=':', alpha=0.7)
        plt.plot(t_63, 0.63, 'ro', markersize=8)
        plt.annotate(f'63% reached at\nt = {t_63:.1f} sec', 
                     xy=(t_63, 0.63), xytext=(t_63+0.5, 0.8),
                     arrowprops=dict(arrowstyle='->', color='red'))
    
    plt.title('What Engineers Measure', fontsize=12)
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\n🎯 SIMPLE TAKEAWAYS:")
    print("• Step response = How system reacts to sudden change")
    print("• Different systems respond differently")
    print("• We measure how FAST and how SMOOTH the response is")
    print("• Engineers use this to design better systems")

def very_simple_motor_example():
    """Super simple motor example"""
    
    print("\n\n🔌 SIMPLE MOTOR EXAMPLE")
    print("=" * 30)
    print()
    print("Imagine you have a small fan motor:")
    print("🔹 You connect it to a battery")
    print("🔹 Does it spin immediately at full speed? NO!")
    print("🔹 It gradually speeds up, right? YES!")
    print()
    print("Let's see what this looks like...")
    
    # Simple motor simulation
    time = np.linspace(0, 3, 300)
    
    # Motor response when we apply voltage
    voltage_applied = np.zeros_like(time)
    voltage_applied[time >= 0.5] = 12  # Apply 12V at t=0.5 seconds
    
    # Motor speed response (starts from 0, gradually reaches final speed)
    motor_speed = np.zeros_like(time)
    for i in range(1, len(time)):
        if time[i] >= 0.5:
            # Simple exponential approach to final speed
            time_since_start = time[i] - 0.5
            max_speed = 1000  # RPM
            motor_speed[i] = max_speed * (1 - np.exp(-time_since_start/0.5))
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(time, voltage_applied, 'r-', linewidth=4, label='Battery Voltage')
    plt.title('What YOU Do: Apply Voltage to Motor', fontsize=14)
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.text(1.5, 6, '← You connect battery here', fontsize=12, 
             bbox=dict(boxstyle='round', facecolor='yellow'))
    
    plt.subplot(2, 1, 2)
    plt.plot(time, motor_speed, 'b-', linewidth=4, label='Motor Speed')
    plt.axhline(y=1000*0.63, color='g', linestyle='--', alpha=0.7, 
                label='63% of max speed')
    plt.title('What MOTOR Does: Gradually Speed Up', fontsize=14)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Motor Speed (RPM)')
    plt.legend()
    plt.grid(True)
    plt.text(1.5, 300, 'Motor takes time\nto speed up!', fontsize=12,
             bbox=dict(boxstyle='round', facecolor='lightblue'))
    
    plt.tight_layout()
    plt.show()
    
    print("\n🎯 WHAT YOU JUST SAW:")
    print("• RED line: You suddenly apply 12V (like flipping a switch)")
    print("• BLUE line: Motor speed gradually increases")
    print("• GREEN line: At this point, motor reached 63% of final speed")
    print()
    print("🤔 WHY DOESN'T MOTOR START INSTANTLY?")
    print("• Motor has inertia (like a heavy wheel)")
    print("• Takes time to overcome friction")
    print("• Electrical currents take time to build up")
    print()
    print("This gradual response curve is called the 'STEP RESPONSE'!")

def explain_why_we_care():
    """Explain why this matters in simple terms"""
    
    print("\n\n🤷‍♂️ WHY DO WE CARE ABOUT THIS?")
    print("=" * 40)
    print()
    print("📱 PRACTICAL EXAMPLES WHERE THIS MATTERS:")
    print()
    print("🚗 CAR CRUISE CONTROL:")
    print("   • You set cruise control to 65 mph")
    print("   • How fast should the car accelerate to 65?")
    print("   • Too slow = frustrated driver")
    print("   • Too fast = jerky, uncomfortable ride")
    print()
    print("🏠 HOUSE THERMOSTAT:")
    print("   • You set temperature to 72°F")
    print("   • How fast should heating system respond?")
    print("   • Too slow = you're cold for too long")
    print("   • Too fast = temperature overshoots, wastes energy")
    print()
    print("🏭 FACTORY ROBOT:")
    print("   • Robot arm needs to move to precise position")
    print("   • How fast should it move?")
    print("   • Too slow = production is slow")
    print("   • Too fast = might overshoot and break things")
    print()
    print("🎯 THE ENGINEERING CHALLENGE:")
    print("Find the RIGHT balance between:")
    print("• FAST response (people don't want to wait)")
    print("• STABLE response (no overshoot or oscillation)")
    print("• ACCURATE response (reach the exact target)")
    print()
    print("That's what control engineers do all day!")

def simple_next_steps():
    """Give encouraging next steps"""
    
    print("\n\n🌟 WHAT'S NEXT? (Don't worry, we'll go slow!)")
    print("=" * 50)
    print()
    print("✅ TODAY YOU LEARNED:")
    print("• What a control system is (measure, compare, adjust)")
    print("• Step response = how systems react to sudden changes")
    print("• Why engineers care about response speed and stability")
    print("• Real examples: cars, thermostats, motors")
    print()
    print("🎯 NEXT BABY STEPS:")
    print("1. Play with the water tank example above")
    print("2. Think about control systems in your daily life")
    print("3. Try changing numbers in the code and see what happens")
    print("4. Don't worry about complex math yet!")
    print()
    print("📚 REMEMBER:")
    print("• Every expert was once a beginner")
    print("• Control systems are just organized common sense")
    print("• You already understand the concepts from daily life")
    print("• The math is just a way to make it precise")
    print()
    print("🚀 WHEN YOU'RE READY:")
    print("• We'll learn about PID controllers (still simple!)")
    print("• We'll see more real examples")
    print("• We'll gradually add math, but always with explanations")
    print()
    print("Don't rush! Understanding is more important than speed.")

def main():
    """Main function to run all basic explanations"""
    
    print("🎓 CONTROL SYSTEMS FOR ABSOLUTE BEGINNERS")
    print("=" * 50)
    print("Don't worry! We'll start from zero and go very slowly.")
    print("Focus on understanding, not memorizing!")
    print("=" * 50)
    
    # Start with the very basics
    explain_basic_concept()
    
    # Simple water tank example
    simple_water_tank_example()
    
    # Explain step response simply
    explain_step_response_simply()
    
    # Simple motor example
    very_simple_motor_example()
    
    # Why it matters
    explain_why_we_care()
    
    # Encouraging next steps
    simple_next_steps()
    
    print("\n" + "=" * 50)
    print("🎉 CONGRATULATIONS!")
    print("You just learned the fundamentals of control systems!")
    print("Everything else builds on these simple concepts.")
    print("=" * 50)

if __name__ == "__main__":
    main()