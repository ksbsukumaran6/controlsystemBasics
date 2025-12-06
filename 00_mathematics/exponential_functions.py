"""
Exponential Functions for Control Systems
========================================

This module demonstrates exponential functions and their properties,
which are fundamental to understanding control system behavior.

Author: Control Systems Learning Guide
Date: November 2025

LEARNING DOCUMENTATION & FUTURE REFERENCE
==========================================

🎯 WHAT ARE EXPONENTIAL FUNCTIONS?
---------------------------------
Exponential functions have the form f(t) = A*e^(at) where:
- A = amplitude/initial value
- a = exponent coefficient (determines growth/decay rate)
- e = Euler's number (≈ 2.718)
- t = independent variable (usually time)

📊 KEY EXPONENTIAL FORMS IN CONTROL SYSTEMS:
-------------------------------------------
1. STEP RESPONSE: y(t) = K(1 - e^(-t/τ))
   - K = steady-state gain
   - τ = time constant
   - Represents how fast system reaches final value

2. IMPULSE RESPONSE: y(t) = (K/τ)e^(-t/τ)
   - Shows natural system behavior
   - Peak occurs at t = 0, decays exponentially

3. NATURAL RESPONSE: y(t) = y₀e^(-t/τ)
   - y₀ = initial condition
   - Shows how system returns to equilibrium

4. COMPLEX EXPONENTIALS: y(t) = Ae^(σt)cos(ωt)
   - σ = real part (determines growth/decay)
   - ω = imaginary part (determines oscillation frequency)
   - Used for oscillatory systems

🔑 CRITICAL CONCEPTS LEARNED:
----------------------------

TIME CONSTANTS (τ):
- Definition: τ = 1/|pole| for first-order systems
- Physical meaning: Time for response to reach 63.2% of final value
- Settling time ≈ 4τ (for 2% criteria)
- Faster systems have smaller τ

STABILITY ANALYSIS:
- Stable: Poles in left half-plane (σ < 0) → e^(σt) decays
- Unstable: Poles in right half-plane (σ > 0) → e^(σt) grows
- Marginal: Poles on imaginary axis (σ = 0) → constant amplitude

SYSTEM RESPONSES:
- Overdamped: Two real poles → sum of exponentials
- Critically damped: Repeated real pole → te^(-t/τ)
- Underdamped: Complex poles → oscillating exponential

📈 PRACTICAL ENGINEERING INSIGHTS:
---------------------------------

RC CIRCUITS:
- Time constant: τ = RC
- Voltage across capacitor: v_c(t) = V(1 - e^(-t/RC))
- Energy storage element creates exponential behavior

DC MOTORS:
- Time constant: τ = J/b (inertia/friction)
- Speed response: ω(t) = (T/b)(1 - e^(-bt/J))
- Mechanical systems follow same exponential laws

TEMPERATURE SYSTEMS:
- Time constant: τ = mc/(hA) (thermal mass/heat transfer)
- Temperature: T(t) = T_∞(1 - e^(-t/τ))
- Thermal systems are typically slow (large τ)

🧮 MATHEMATICAL PROPERTIES TO REMEMBER:
--------------------------------------

DERIVATIVES:
- d/dt[e^(at)] = a·e^(at)
- The exponential function is its own derivative (scaled)

INTEGRALS:
- ∫e^(at)dt = (1/a)e^(at) + C
- Exponentials integrate to exponentials

LAPLACE TRANSFORMS:
- L{e^(at)} = 1/(s-a)
- L{e^(-at)} = 1/(s+a)
- This is why transfer functions have exponential responses

SUPERPOSITION:
- Sum of exponentials = sum of individual responses
- Linear systems allow this principle

⚡ PERFORMANCE METRICS:
----------------------

RISE TIME: Time to go from 10% to 90% of final value
- For first-order: t_r ≈ 2.2τ

SETTLING TIME: Time to stay within ±2% of final value
- For first-order: t_s ≈ 4τ
- For second-order: depends on damping ratio

OVERSHOOT: Maximum deviation above final value
- No overshoot for first-order systems
- Related to damping in second-order systems

💡 DESIGN IMPLICATIONS:
----------------------

FAST RESPONSE: Small time constant (τ)
- Requires high bandwidth
- More sensitive to noise
- Higher control effort

SLOW RESPONSE: Large time constant (τ)
- More stable and robust
- Less sensitive to disturbances
- Lower control effort

TRADE-OFFS:
- Speed vs Stability
- Performance vs Robustness
- Control effort vs Response time

🎯 CONNECTION TO CONTROL THEORY:
-------------------------------

TRANSFER FUNCTIONS:
- Poles determine exponential behavior
- G(s) = K/(τs + 1) → step response = K(1 - e^(-t/τ))

CONTROLLER DESIGN:
- Pole placement affects time constants
- Faster poles → faster response
- Controller adds poles/zeros → changes exponential behavior

FREQUENCY DOMAIN:
- Exponentials ↔ Complex frequency (s-domain)
- Bode plots show frequency response of exponential systems
- Phase lag related to exponential delay

📚 STUDY CHECKLIST - MASTERY INDICATORS:
---------------------------------------
□ Can plot basic exponentials (growth/decay)
□ Understand time constant physical meaning
□ Calculate settling time from time constant
□ Identify stable vs unstable exponential behavior
□ Connect pole locations to exponential responses
□ Analyze step/impulse responses
□ Apply exponential analysis to real systems (RC, motor, thermal)
□ Use exponentials to predict system performance
□ Understand trade-offs in exponential response design

🔄 PRACTICE EXERCISES COMPLETED:
-------------------------------
□ Plotted various exponential functions
□ Analyzed different time constants
□ Connected math to physical systems
□ Explored stability through exponential behavior
□ Compared system responses
□ Applied to engineering examples

💼 REAL-WORLD APPLICATIONS UNDERSTOOD:
-------------------------------------
□ Electrical circuits (RC charging/discharging)
□ Mechanical systems (motor speed control)
□ Thermal systems (temperature regulation)
□ Control system design implications
□ Performance vs stability trade-offs

🚀 NEXT LEARNING STEPS:
----------------------
1. Complex numbers and Euler's formula
2. Laplace transforms of exponentials
3. Second-order systems and damping
4. Root locus and exponential behavior
5. Frequency domain analysis
6. Controller design using exponential concepts

🎓 MASTERY ACHIEVED WHEN:
------------------------
- You can predict system behavior from exponential analysis
- You understand time constants in any physical system
- You can design for desired exponential response
- You connect time domain exponentials to frequency domain
- You use exponential insights for controller design

Remember: Exponential functions are the foundation of linear system analysis.
Master these concepts and control systems become much more intuitive!
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy import signal
import math

def plot_basic_exponentials():
    """Plot basic exponential functions: e^x, e^(-x), and e^(ax)"""
    
    # Create time array
    t = np.linspace(-3, 3, 1000)
    
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Basic exponential e^x
    plt.subplot(2, 3, 1)
    y1 = np.exp(t)
    plt.plot(t, y1, 'b-', linewidth=2, label='$e^t$')
    plt.title('Basic Exponential: $e^t$')
    plt.xlabel('t')
    plt.ylabel('$e^t$')
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 20)
    
    # Plot 2: Decaying exponential e^(-x)
    plt.subplot(2, 3, 2)
    y2 = np.exp(-t)
    plt.plot(t, y2, 'r-', linewidth=2, label='$e^{-t}$')
    plt.title('Decaying Exponential: $e^{-t}$')
    plt.xlabel('t')
    plt.ylabel('$e^{-t}$')
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 20)
    
    # Plot 3: Different decay rates
    plt.subplot(2, 3, 3)
    a_values = [0.5, 1, 2, 5]
    colors = ['green', 'red', 'blue', 'orange']
    
    for a, color in zip(a_values, colors):
        y = np.exp(-a * t)
        plt.plot(t, y, color=color, linewidth=2, label=f'$e^{{-{a}t}}$')
    
    plt.title('Different Decay Rates')
    plt.xlabel('t')
    plt.ylabel('$e^{-at}$')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 3)
    plt.ylim(0, 1.1)
    
    # Plot 4: Growing exponentials with different rates
    plt.subplot(2, 3, 4)
    for a, color in zip(a_values, colors):
        y = np.exp(a * t)
        plt.plot(t, y, color=color, linewidth=2, label=f'$e^{{{a}t}}$')
    
    plt.title('Different Growth Rates')
    plt.xlabel('t')
    plt.ylabel('$e^{at}$')
    plt.grid(True)
    plt.legend()
    plt.xlim(-1, 1)
    plt.ylim(0, 20)
    
    # Plot 5: Time constants demonstration
    plt.subplot(2, 3, 5)
    tau_values = [0.5, 1, 2, 4]  # Time constants
    
    for tau, color in zip(tau_values, colors):
        y = 1 - np.exp(-t/tau)  # Step response form
        plt.plot(t, y, color=color, linewidth=2, label=f'τ = {tau}')
        
        # Mark 63.2% point (1 time constant)
        if tau == 2:  # Highlight one example
            plt.axvline(x=tau, color=color, linestyle='--', alpha=0.7)
            plt.axhline(y=0.632, color=color, linestyle='--', alpha=0.7)
            plt.plot(tau, 0.632, 'ko', markersize=8)
            plt.annotate(f'63.2% at t=τ={tau}', 
                        xy=(tau, 0.632), xytext=(tau+0.5, 0.8),
                        arrowprops=dict(arrowstyle='->', color='black'))
    
    plt.title('Time Constants in Step Response')
    plt.xlabel('t (seconds)')
    plt.ylabel('Response')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 8)
    plt.ylim(0, 1.1)
    
    # Plot 6: Complex exponentials (real part)
    plt.subplot(2, 3, 6)
    omega = 2  # frequency
    sigma_values = [-0.5, 0, 0.5]
    
    for sigma in sigma_values:
        y = np.exp(sigma * t) * np.cos(omega * t)
        if sigma < 0:
            plt.plot(t, y, 'b-', linewidth=2, label=f'$e^{{{sigma}t}}\\cos({omega}t)$ (Decaying)')
        elif sigma == 0:
            plt.plot(t, y, 'g-', linewidth=2, label=f'$\\cos({omega}t)$ (Sustained)')
        else:
            plt.plot(t, y, 'r-', linewidth=2, label=f'$e^{{{sigma}t}}\\cos({omega}t)$ (Growing)')
    
    plt.title('Complex Exponentials (Real Part)')
    plt.xlabel('t')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.xlim(-3, 3)
    
    plt.tight_layout()
    plt.show()

def control_system_exponentials():
    """Demonstrate exponential functions in control systems context"""
    
    print("=== Exponential Functions in Control Systems ===\n")
    
    # Time vector
    t = np.linspace(0, 10, 1000)
    
    plt.figure(figsize=(15, 12))
    
    # 1. First-order system step response
    plt.subplot(2, 3, 1)
    tau = 2.0  # Time constant
    K = 1.0    # Gain
    
    # Step response: y(t) = K(1 - e^(-t/τ))
    step_response = K * (1 - np.exp(-t/tau))
    plt.plot(t, step_response, 'b-', linewidth=3, label='Step Response')
    
    # Mark important points
    plt.axhline(y=K*0.632, color='r', linestyle='--', alpha=0.7, label='63.2% (1τ)')
    plt.axhline(y=K*0.950, color='g', linestyle='--', alpha=0.7, label='95% (3τ)')
    plt.axhline(y=K*0.982, color='orange', linestyle='--', alpha=0.7, label='98.2% (4τ)')
    
    plt.axvline(x=tau, color='r', linestyle='--', alpha=0.7)
    plt.axvline(x=3*tau, color='g', linestyle='--', alpha=0.7)
    plt.axvline(x=4*tau, color='orange', linestyle='--', alpha=0.7)
    
    plt.title(f'First-Order System Step Response (τ = {tau}s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Output')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 10)
    
    # 2. Impulse response
    plt.subplot(2, 3, 2)
    impulse_response = (K/tau) * np.exp(-t/tau)
    plt.plot(t, impulse_response, 'r-', linewidth=3)
    plt.title('Impulse Response: $\\frac{K}{τ}e^{-t/τ}$')
    plt.xlabel('Time (s)')
    plt.ylabel('Output')
    plt.grid(True)
    
    # 3. Different system poles
    plt.subplot(2, 3, 3)
    poles = [-0.5, -1, -2, -5]  # Different pole locations
    colors = ['blue', 'green', 'red', 'orange']
    
    for pole, color in zip(poles, colors):
        response = np.exp(pole * t)
        plt.plot(t, response, color=color, linewidth=2, 
                label=f'Pole at s = {pole}')
    
    plt.title('System Response vs Pole Location')
    plt.xlabel('Time (s)')
    plt.ylabel('$e^{pt}$')
    plt.grid(True)
    plt.legend()
    plt.yscale('log')
    
    # 4. Stability regions
    plt.subplot(2, 3, 4)
    
    # Stable system (pole in left half-plane)
    stable_response = np.exp(-t)
    plt.plot(t, stable_response, 'g-', linewidth=3, label='Stable (p < 0)')
    
    # Marginally stable (pole on imaginary axis)
    marginal_response = np.ones_like(t)
    plt.plot(t, marginal_response, 'y-', linewidth=3, label='Marginal (p = 0)')
    
    # Unstable system (pole in right half-plane)
    unstable_response = np.exp(0.2 * t)
    plt.plot(t, unstable_response, 'r-', linewidth=3, label='Unstable (p > 0)')
    
    plt.title('Stability and Pole Locations')
    plt.xlabel('Time (s)')
    plt.ylabel('Response')
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 5)
    
    # 5. Oscillatory systems
    plt.subplot(2, 3, 5)
    omega_n = 2  # Natural frequency
    zeta_values = [0.1, 0.3, 0.7, 1.0]  # Damping ratios
    
    for zeta in zeta_values:
        if zeta < 1:
            omega_d = omega_n * np.sqrt(1 - zeta**2)
            response = np.exp(-zeta * omega_n * t) * np.cos(omega_d * t)
            plt.plot(t, response, linewidth=2, label=f'ζ = {zeta}')
        else:
            response = np.exp(-omega_n * t)
            plt.plot(t, response, linewidth=2, label=f'ζ = {zeta} (overdamped)')
    
    plt.title('Damped Oscillations: $e^{-\\zeta\\omega_nt}\\cos(\\omega_dt)$')
    plt.xlabel('Time (s)')
    plt.ylabel('Response')
    plt.grid(True)
    plt.legend()
    
    # 6. Time constant analysis
    plt.subplot(2, 3, 6)
    
    # Show settling time for different time constants
    tau_values = [0.5, 1, 2, 4]
    
    for i, tau in enumerate(tau_values):
        response = 1 - np.exp(-t/tau)
        plt.plot(t, response + i*1.2, linewidth=2, label=f'τ = {tau}s')
        
        # Mark settling time (4τ for 2% criteria)
        settling_time = 4 * tau
        if settling_time < 10:
            plt.axvline(x=settling_time, 
                       ymin=i*0.24, ymax=(i+1)*0.24,
                       color='red', linestyle='--', alpha=0.7)
    
    plt.title('Settling Time vs Time Constant')
    plt.xlabel('Time (s)')
    plt.ylabel('Response (offset for clarity)')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 10)
    
    plt.tight_layout()
    plt.show()

def exponential_properties():
    """Demonstrate mathematical properties of exponentials"""
    
    print("\n=== Mathematical Properties of Exponentials ===\n")
    
    # Symbolic mathematics with SymPy
    t, a, b = sp.symbols('t a b', real=True)
    
    print("1. Basic Exponential Properties:")
    print("   e^0 =", sp.exp(0))
    print("   e^1 =", sp.exp(1).evalf())
    print("   e^(a+b) = e^a * e^b")
    print("   e^(a-b) = e^a / e^b")
    print("   (e^a)^b = e^(a*b)")
    
    print("\n2. Derivative Properties:")
    exp_func = sp.exp(a*t)
    derivative = sp.diff(exp_func, t)
    print(f"   d/dt[e^(at)] = {derivative}")
    
    print("\n3. Integral Properties:")
    integral = sp.integrate(exp_func, t)
    print(f"   ∫e^(at)dt = {integral}")
    
    print("\n4. Laplace Transform:")
    s = sp.symbols('s')
    # Note: SymPy's laplace_transform requires specific setup
    print("   L{e^(at)} = 1/(s-a)")
    print("   L{e^(-at)} = 1/(s+a)")
    
    # Numerical verification
    print("\n5. Numerical Examples:")
    print("   e^(-1) ≈", math.exp(-1))
    print("   e^(-2) ≈", math.exp(-2))
    print("   e^(-5) ≈", math.exp(-5))
    
    print("\n6. Time Constant Relationship:")
    print("   For τ = 1/a in e^(-t/τ) = e^(-at)")
    print("   When t = τ, the value is e^(-1) ≈ 0.368")
    print("   So the output is 63.2% of final value at t = τ")

def practical_examples():
    """Show practical control system examples using exponentials"""
    
    print("\n=== Practical Control System Examples ===\n")
    
    # Example 1: RC Circuit
    print("Example 1: RC Circuit (First-Order System)")
    R = 1000  # Resistance in ohms
    C = 1e-3  # Capacitance in farads
    tau_rc = R * C  # Time constant
    print(f"   R = {R} Ω, C = {C*1000} mF")
    print(f"   Time constant τ = RC = {tau_rc} seconds")
    
    t = np.linspace(0, 5*tau_rc, 1000)
    
    plt.figure(figsize=(12, 8))
    
    # Step response
    plt.subplot(2, 2, 1)
    v_step = 5  # 5V step input
    v_c = v_step * (1 - np.exp(-t/tau_rc))
    plt.plot(t, v_c, 'b-', linewidth=3)
    plt.axhline(y=v_step*0.632, color='r', linestyle='--', alpha=0.7)
    plt.axvline(x=tau_rc, color='r', linestyle='--', alpha=0.7)
    plt.title('RC Circuit Step Response')
    plt.xlabel('Time (s)')
    plt.ylabel('Capacitor Voltage (V)')
    plt.grid(True)
    
    # Example 2: Motor speed control
    print(f"\nExample 2: DC Motor Speed Control")
    J = 0.01   # Inertia
    b = 0.1    # Friction coefficient
    tau_motor = J/b
    print(f"   Inertia J = {J} kg⋅m²")
    print(f"   Friction b = {b} N⋅m⋅s")
    print(f"   Time constant τ = J/b = {tau_motor} seconds")
    
    plt.subplot(2, 2, 2)
    torque_step = 1  # 1 N⋅m step torque
    omega = (torque_step/b) * (1 - np.exp(-t/tau_motor))
    plt.plot(t, omega, 'g-', linewidth=3)
    plt.title('Motor Speed Response')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (rad/s)')
    plt.grid(True)
    
    # Example 3: Temperature control
    print(f"\nExample 3: Temperature Control System")
    m = 2      # Mass in kg
    c = 4186   # Specific heat capacity (water)
    h = 50     # Heat transfer coefficient
    A = 0.1    # Surface area
    tau_temp = (m * c) / (h * A)
    print(f"   Mass m = {m} kg")
    print(f"   Heat capacity c = {c} J/(kg⋅K)")
    print(f"   Time constant τ = mc/(hA) = {tau_temp:.1f} seconds")
    
    plt.subplot(2, 2, 3)
    t_temp = np.linspace(0, 3*tau_temp, 1000)
    temp_rise = 20  # 20°C temperature rise
    temp_response = temp_rise * (1 - np.exp(-t_temp/tau_temp))
    plt.plot(t_temp, temp_response, 'r-', linewidth=3)
    plt.title('Temperature Response')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature Rise (°C)')
    plt.grid(True)
    
    # Example 4: Comparison of systems
    plt.subplot(2, 2, 4)
    t_norm = np.linspace(0, 5, 1000)
    
    # Normalized responses (all with different time constants)
    systems = [
        ('RC Circuit', tau_rc, 'blue'),
        ('Motor', tau_motor, 'green'),
        ('Temperature', tau_temp/100, 'red')  # Scaled for visibility
    ]
    
    for name, tau, color in systems:
        response = 1 - np.exp(-t_norm/tau)
        plt.plot(t_norm, response, color=color, linewidth=2, label=f'{name} (τ={tau:.3f})')
    
    plt.title('Normalized System Responses')
    plt.xlabel('Time / τ')
    plt.ylabel('Normalized Response')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run all demonstrations"""
    
    print("=" * 60)
    print("EXPONENTIAL FUNCTIONS FOR CONTROL SYSTEMS")
    print("=" * 60)
    
    # Display basic exponential plots
    plot_basic_exponentials()
    
    # Show exponential properties
    exponential_properties()
    
    # Control system specific examples
    control_system_exponentials()
    
    # Practical examples
    practical_examples()
    
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("=" * 60)
    print("1. Exponential functions describe natural system responses")
    print("2. Time constants determine how fast systems respond")
    print("3. Pole locations (in s-plane) determine stability")
    print("4. e^(-t/τ) represents decay, e^(t/τ) represents growth")
    print("5. At t = τ, the response reaches 63.2% of final value")
    print("6. Settling time ≈ 4τ (for 2% criteria)")
    print("7. Complex exponentials create oscillatory responses")
    print("=" * 60)
    
    print("\n" + "🎓 LEARNING SUMMARY" + "=" * 44)
    print("✅ CONCEPTS DEMONSTRATED:")
    print("   • Basic exponential functions and their properties")
    print("   • Time constants and their physical meaning")
    print("   • System stability through exponential analysis")
    print("   • Step and impulse responses")
    print("   • Real-world engineering applications")
    print("   • Mathematical properties and Laplace connections")
    print("\n✅ SKILLS DEVELOPED:")
    print("   • Plotting and interpreting exponential functions")
    print("   • Connecting math to physical system behavior")
    print("   • Analyzing system speed and stability")
    print("   • Understanding design trade-offs")
    print("\n✅ READY FOR NEXT STEPS:")
    print("   • Complex numbers and oscillatory systems")
    print("   • Laplace transforms and transfer functions")
    print("   • Second-order system analysis")
    print("   • Controller design principles")
    print("=" * 60)
    
    print("\n📝 STUDY NOTES:")
    print("View the comprehensive learning documentation at the top")
    print("of this file for detailed explanations and future reference.")
    print("=" * 60)

if __name__ == "__main__":
    main()