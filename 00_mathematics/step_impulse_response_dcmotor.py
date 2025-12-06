"""
Step and Impulse Response Analysis for DC Motor Control
=====================================================

This module demonstrates step and impulse response analysis with practical
DC motor control examples, including how to work with real experimental data.

Author: Control Systems Learning Guide
Date: December 2025

LEARNING DOCUMENTATION & FUTURE REFERENCE
==========================================

🎯 WHAT ARE STEP AND IMPULSE RESPONSES?
--------------------------------------
STEP RESPONSE:
- System's output when input suddenly changes from 0 to a constant value
- Shows: settling time, overshoot, steady-state error, rise time
- Physical meaning: How motor responds to sudden voltage change

IMPULSE RESPONSE:
- System's output when input is a very brief, high-intensity pulse
- Shows: natural system behavior, transient characteristics
- Physical meaning: Motor's reaction to instantaneous torque/voltage spike

📊 KEY PERFORMANCE METRICS:
--------------------------
RISE TIME (tr): Time to go from 10% to 90% of final value
SETTLING TIME (ts): Time to stay within ±2% of final value  
OVERSHOOT (%OS): Maximum deviation above final value
STEADY-STATE ERROR (ess): Final difference between desired and actual output
PEAK TIME (tp): Time to reach maximum overshoot

🔧 DC MOTOR SYSTEM CHARACTERISTICS:
----------------------------------
TRANSFER FUNCTION: G(s) = K / (τs + 1)(Js + b)
Where:
- K = motor gain (speed/voltage or position/voltage)
- τ = electrical time constant (L/R)
- J = rotor inertia
- b = viscous friction coefficient

TYPICAL PARAMETERS:
- Electrical time constant: τe = L/R ≈ 0.001-0.01 s (fast)
- Mechanical time constant: τm = J/b ≈ 0.1-1.0 s (slower)
- Motor gain: K depends on motor specifications

🎯 PRACTICAL APPLICATIONS:
-------------------------
POSITION CONTROL: Robot arm, CNC machine, servo systems
SPEED CONTROL: Conveyor belt, fan, pump, vehicle cruise control
CURRENT CONTROL: Torque regulation, protection against overcurrent

📈 DATA ANALYSIS WORKFLOW:
-------------------------
1. COLLECT DATA: Time, input voltage, output (speed/position)
2. IDENTIFY SYSTEM: Estimate transfer function from data
3. VALIDATE MODEL: Compare model response with experimental data
4. DESIGN CONTROLLER: Based on desired performance specifications
5. IMPLEMENT & TEST: Real-world validation

🧮 MATHEMATICAL RELATIONSHIPS:
-----------------------------
For first-order system: G(s) = K/(τs + 1)
- Step response: y(t) = K(1 - e^(-t/τ))
- Impulse response: y(t) = (K/τ)e^(-t/τ)
- Time constant: τ = time to reach 63.2% of final value

For second-order system: G(s) = ωn²/(s² + 2ζωns + ωn²)
- Natural frequency: ωn (rad/s)
- Damping ratio: ζ
- Overshoot: %OS = 100 × e^(-ζπ/√(1-ζ²))
- Settling time: ts ≈ 4/(ζωn)

🎓 DESIGN INSIGHTS:
------------------
UNDERDAMPED (ζ < 1): Fast response, some overshoot, oscillatory
CRITICALLY DAMPED (ζ = 1): Fastest response without overshoot
OVERDAMPED (ζ > 1): Slow response, no overshoot, sluggish

TRADE-OFFS:
- Speed vs Stability
- Overshoot vs Settling time
- Performance vs Robustness
- Energy consumption vs Response time
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import control as ct
from scipy.optimize import curve_fit
from scipy import interpolate
import pandas as pd

class DCMotorAnalyzer:
    """Class to analyze DC motor step and impulse responses"""
    
    def __init__(self, motor_params=None):
        """
        Initialize DC motor analyzer with default or custom parameters
        
        Parameters:
        motor_params (dict): Dictionary containing motor parameters
                           {'K': gain, 'tau': time_constant, 'J': inertia, 'b': friction}
        """
        if motor_params is None:
            # Default small DC motor parameters
            self.params = {
                'K': 1.0,      # Motor gain (rpm/V or rad/s/V)
                'tau_e': 0.005,  # Electrical time constant (s)
                'tau_m': 0.2,    # Mechanical time constant (s)
                'J': 0.01,     # Rotor inertia (kg⋅m²)
                'b': 0.05      # Viscous friction (N⋅m⋅s)
            }
        else:
            self.params = motor_params
        
        # Create transfer function
        self._create_transfer_function()
    
    def _create_transfer_function(self):
        """Create motor transfer function from parameters"""
        K = self.params['K']
        tau_e = self.params['tau_e']
        tau_m = self.params['tau_m']
        
        # First-order approximation (electrical much faster than mechanical)
        if tau_e < 0.1 * tau_m:
            # G(s) = K / (τs + 1)
            self.tf = ct.TransferFunction([K], [tau_m, 1])
            self.model_type = "First-order"
        else:
            # Second-order system
            # G(s) = K / ((τ_e*s + 1)(τ_m*s + 1))
            num = [K]
            den = np.convolve([tau_e, 1], [tau_m, 1])  # Multiply polynomials
            self.tf = ct.TransferFunction(num, den)
            self.model_type = "Second-order"
    
    def generate_synthetic_data(self, test_type='step', noise_level=0.02, duration=2.0):
        """
        Generate synthetic experimental data for testing
        
        Parameters:
        test_type (str): 'step', 'impulse', or 'custom'
        noise_level (float): Standard deviation of measurement noise
        duration (float): Test duration in seconds
        
        Returns:
        time, input_signal, output_signal (numpy arrays)
        """
        dt = 0.01  # Sample time
        time = np.arange(0, duration, dt)
        
        if test_type == 'step':
            # Step input at t = 0.1s
            input_signal = np.zeros_like(time)
            input_signal[time >= 0.1] = 5.0  # 5V step
            
            # Generate true response
            t_response, y_true = ct.step_response(self.tf * 5.0, time)
            
        elif test_type == 'impulse':
            # Impulse approximation (short pulse)
            input_signal = np.zeros_like(time)
            pulse_width = 5  # samples
            input_signal[10:10+pulse_width] = 10.0 / (pulse_width * dt)  # Normalize
            
            # Generate response using lsim
            t_response, y_true, _ = ct.forced_response(self.tf, time, input_signal)
            
        elif test_type == 'custom':
            # Custom input (ramp + step)
            input_signal = np.zeros_like(time)
            ramp_end = len(time) // 3
            step_start = 2 * len(time) // 3
            
            input_signal[:ramp_end] = 3.0 * time[:ramp_end] / time[ramp_end]
            input_signal[step_start:] = 6.0
            
            t_response, y_true, _ = ct.forced_response(self.tf, time, input_signal)
        
        # Add realistic noise
        noise = np.random.normal(0, noise_level * np.max(y_true), len(y_true))
        output_signal = y_true + noise
        
        return time, input_signal, output_signal, y_true
    
    def analyze_step_response(self, time_data=None, output_data=None, plot=True):
        """
        Analyze step response and extract performance metrics
        
        Parameters:
        time_data, output_data: Experimental data (optional)
        plot (bool): Whether to create plots
        
        Returns:
        metrics (dict): Performance metrics
        """
        if time_data is None or output_data is None:
            # Use theoretical response
            time_data, y_data = ct.step_response(self.tf)
            data_type = "Theoretical"
        else:
            y_data = output_data
            data_type = "Experimental"
        
        # Calculate performance metrics
        final_value = y_data[-1]
        
        # Rise time (10% to 90%)
        idx_10 = np.where(y_data >= 0.1 * final_value)[0]
        idx_90 = np.where(y_data >= 0.9 * final_value)[0]
        
        if len(idx_10) > 0 and len(idx_90) > 0:
            rise_time = time_data[idx_90[0]] - time_data[idx_10[0]]
        else:
            rise_time = float('inf')
        
        # Settling time (2% criterion)
        settling_band = 0.02 * abs(final_value)
        settled_indices = np.where(np.abs(y_data - final_value) <= settling_band)[0]
        
        if len(settled_indices) > 0:
            settling_time = time_data[settled_indices[0]]
        else:
            settling_time = float('inf')
        
        # Overshoot
        max_value = np.max(y_data)
        overshoot_percent = 100 * (max_value - final_value) / final_value if final_value != 0 else 0
        
        # Peak time
        peak_index = np.argmax(y_data)
        peak_time = time_data[peak_index]
        
        metrics = {
            'rise_time': rise_time,
            'settling_time': settling_time,
            'overshoot_percent': overshoot_percent,
            'peak_time': peak_time,
            'final_value': final_value,
            'max_value': max_value
        }
        
        if plot:
            self._plot_step_analysis(time_data, y_data, metrics, data_type)
        
        return metrics
    
    def _plot_step_analysis(self, time, output, metrics, data_type):
        """Plot step response with performance metrics annotated"""
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        plt.plot(time, output, 'b-', linewidth=2, label=f'{data_type} Response')
        
        # Mark performance metrics
        final_val = metrics['final_value']
        
        # Final value line
        plt.axhline(y=final_val, color='k', linestyle='--', alpha=0.5, label='Final Value')
        
        # 10% and 90% lines for rise time
        plt.axhline(y=0.1*final_val, color='g', linestyle=':', alpha=0.7)
        plt.axhline(y=0.9*final_val, color='g', linestyle=':', alpha=0.7)
        
        # Settling time region
        settling_band = 0.02 * abs(final_val)
        plt.axhline(y=final_val + settling_band, color='r', linestyle=':', alpha=0.5)
        plt.axhline(y=final_val - settling_band, color='r', linestyle=':', alpha=0.5)
        plt.axvline(x=metrics['settling_time'], color='r', linestyle='--', alpha=0.7, label='Settling Time')
        
        # Overshoot
        if metrics['overshoot_percent'] > 0:
            plt.axhline(y=metrics['max_value'], color='orange', linestyle=':', alpha=0.7)
            plt.axvline(x=metrics['peak_time'], color='orange', linestyle='--', alpha=0.7, label='Peak Time')
        
        plt.title('Step Response Analysis')
        plt.xlabel('Time (s)')
        plt.ylabel('Output')
        plt.legend()
        plt.grid(True)
        
        # Performance metrics text
        plt.subplot(2, 1, 2)
        metrics_text = f"""
        PERFORMANCE METRICS ({data_type}):
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Rise Time (10%-90%):    {metrics['rise_time']:.3f} s
        Settling Time (2%):     {metrics['settling_time']:.3f} s
        Overshoot:             {metrics['overshoot_percent']:.1f} %
        Peak Time:             {metrics['peak_time']:.3f} s
        Final Value:           {metrics['final_value']:.3f}
        Peak Value:            {metrics['max_value']:.3f}
        
        SYSTEM PARAMETERS:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Motor Gain (K):        {self.params['K']:.3f}
        Electrical τ:          {self.params['tau_e']:.4f} s
        Mechanical τ:          {self.params['tau_m']:.3f} s
        Model Type:            {self.model_type}
        """
        
        plt.text(0.05, 0.95, metrics_text, transform=plt.gca().transAxes, 
                fontfamily='monospace', fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def compare_responses(self, parameter_variations):
        """
        Compare step responses for different parameter values
        
        Parameters:
        parameter_variations (dict): Parameter name and list of values to test
        """
        plt.figure(figsize=(15, 10))
        
        base_params = self.params.copy()
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
        
        for param_name, param_values in parameter_variations.items():
            plt.subplot(2, 2, 1)
            
            for i, param_value in enumerate(param_values):
                # Modify parameter
                test_params = base_params.copy()
                test_params[param_name] = param_value
                
                # Create temporary motor with new parameters
                temp_motor = DCMotorAnalyzer(test_params)
                
                # Generate step response
                time, y = ct.step_response(temp_motor.tf)
                
                color = colors[i % len(colors)]
                plt.plot(time, y, color=color, linewidth=2, 
                        label=f'{param_name}={param_value}')
            
            plt.title(f'Effect of {param_name} on Step Response')
            plt.xlabel('Time (s)')
            plt.ylabel('Output')
            plt.legend()
            plt.grid(True)
    
    def system_identification_from_data(self, time, input_signal, output_signal, plot=True):
        """
        Identify system parameters from experimental step response data
        
        Parameters:
        time, input_signal, output_signal: Experimental data arrays
        plot (bool): Whether to show identification results
        
        Returns:
        identified_params (dict): Estimated system parameters
        """
        # Find step start and steady-state value
        step_start_idx = np.where(np.diff(input_signal) > 0.1)[0]
        if len(step_start_idx) > 0:
            step_start = step_start_idx[0]
            step_amplitude = input_signal[step_start + 10]  # After transient
        else:
            step_start = 0
            step_amplitude = np.mean(input_signal[len(input_signal)//2:])
        
        # Extract step response portion
        response_start = step_start
        time_response = time[response_start:] - time[response_start]
        output_response = output_signal[response_start:]
        
        # Estimate steady-state gain
        steady_state_output = np.mean(output_response[-50:])  # Average last 50 points
        estimated_K = steady_state_output / step_amplitude
        
        # Fit first-order model: y(t) = K*(1 - exp(-t/tau))
        def first_order_step(t, K, tau):
            return K * (1 - np.exp(-t/tau))
        
        try:
            # Initial guess
            p0 = [estimated_K, 0.2]
            
            # Fit the model
            popt, pcov = curve_fit(first_order_step, time_response, output_response, 
                                 p0=p0, bounds=([0, 0.001], [10*estimated_K, 5.0]))
            
            identified_K, identified_tau = popt
            
            # Calculate fit quality
            fitted_response = first_order_step(time_response, identified_K, identified_tau)
            r_squared = 1 - (np.sum((output_response - fitted_response)**2) / 
                            np.sum((output_response - np.mean(output_response))**2))
            
            identified_params = {
                'K': identified_K,
                'tau': identified_tau,
                'fit_quality': r_squared,
                'steady_state': steady_state_output
            }
            
            if plot:
                self._plot_identification_results(time, input_signal, output_signal,
                                                time_response, fitted_response, 
                                                identified_params)
            
            return identified_params
            
        except Exception as e:
            print(f"System identification failed: {e}")
            return None
    
    def _plot_identification_results(self, time, input_signal, output_signal,
                                   time_response, fitted_response, params):
        """Plot system identification results"""
        plt.figure(figsize=(15, 10))
        
        # Plot 1: Original data and fitted model
        plt.subplot(2, 2, 1)
        plt.plot(time, output_signal, 'b-', linewidth=2, label='Experimental Data')
        
        # Overlay fitted response
        fit_time = time_response + time[0]
        plt.plot(fit_time, fitted_response, 'r--', linewidth=2, label='Fitted Model')
        
        plt.title('System Identification Results')
        plt.xlabel('Time (s)')
        plt.ylabel('Output')
        plt.legend()
        plt.grid(True)
        
        # Plot 2: Input signal
        plt.subplot(2, 2, 2)
        plt.plot(time, input_signal, 'g-', linewidth=2)
        plt.title('Input Signal')
        plt.xlabel('Time (s)')
        plt.ylabel('Input')
        plt.grid(True)
        
        # Plot 3: Residuals
        plt.subplot(2, 2, 3)
        residuals = output_signal[len(output_signal)-len(fitted_response):] - fitted_response
        plt.plot(time_response, residuals, 'r-', linewidth=1)
        plt.title('Model Residuals')
        plt.xlabel('Time (s)')
        plt.ylabel('Error')
        plt.grid(True)
        
        # Plot 4: Identification summary
        plt.subplot(2, 2, 4)
        summary_text = f"""
        IDENTIFIED PARAMETERS:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Motor Gain (K):      {params['K']:.3f}
        Time Constant (τ):   {params['tau']:.3f} s
        Steady-State Value:  {params['steady_state']:.3f}
        Fit Quality (R²):    {params['fit_quality']:.3f}
        
        MODEL EQUATION:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        G(s) = {params['K']:.3f} / ({params['tau']:.3f}s + 1)
        
        Step Response:
        y(t) = {params['K']:.3f}(1 - e^(-t/{params['tau']:.3f}))
        
        PERFORMANCE ESTIMATES:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        63.2% Value at:      {params['tau']:.3f} s
        Settling Time (~4τ): {4*params['tau']:.3f} s
        """
        
        plt.text(0.05, 0.95, summary_text, transform=plt.gca().transAxes,
                fontfamily='monospace', fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()

def practical_dc_motor_examples():
    """Demonstrate practical DC motor control examples"""
    
    print("=" * 70)
    print("PRACTICAL DC MOTOR STEP & IMPULSE RESPONSE ANALYSIS")
    print("=" * 70)
    
    # Example 1: Small servo motor
    print("\n📡 EXAMPLE 1: Small Servo Motor (Position Control)")
    print("-" * 50)
    
    servo_params = {
        'K': 2.5,        # Position gain (rad/V)
        'tau_e': 0.002,  # Fast electrical response
        'tau_m': 0.15,   # Mechanical time constant
        'J': 0.005,      # Small inertia
        'b': 0.033       # Moderate friction
    }
    
    servo_motor = DCMotorAnalyzer(servo_params)
    print(f"Transfer Function: {servo_motor.tf}")
    
    # Generate synthetic experimental data
    time, input_voltage, position_data, true_response = servo_motor.generate_synthetic_data(
        test_type='step', noise_level=0.03, duration=1.5)
    
    # Analyze step response
    metrics = servo_motor.analyze_step_response(time, position_data, plot=True)
    
    # System identification
    print("\n🔍 System Identification from 'Experimental' Data:")
    identified = servo_motor.system_identification_from_data(time, input_voltage, position_data)
    
    if identified:
        print(f"Original K: {servo_params['K']:.3f}, Identified K: {identified['K']:.3f}")
        print(f"Original τ: {servo_params['tau_m']:.3f}, Identified τ: {identified['tau']:.3f}")
        print(f"Fit Quality (R²): {identified['fit_quality']:.3f}")
    
    # Example 2: Industrial motor
    print("\n\n🏭 EXAMPLE 2: Industrial Motor (Speed Control)")
    print("-" * 50)
    
    industrial_params = {
        'K': 15.0,       # Speed gain (rpm/V)
        'tau_e': 0.008,  # Electrical time constant
        'tau_m': 0.5,    # Larger mechanical time constant
        'J': 0.2,        # Larger inertia
        'b': 0.4         # Higher friction
    }
    
    industrial_motor = DCMotorAnalyzer(industrial_params)
    
    # Compare different loading conditions
    load_variations = {
        'tau_m': [0.3, 0.5, 0.8, 1.2]  # Different mechanical time constants (loads)
    }
    
    print("Comparing different load conditions...")
    industrial_motor.compare_responses(load_variations)
    
    plt.suptitle('Effect of Load Changes on Industrial Motor Response')
    plt.show()
    
    # Example 3: Real data analysis workflow
    print("\n\n📊 EXAMPLE 3: Working with Real Experimental Data")
    print("-" * 50)
    
    # Simulate realistic experimental data with measurement artifacts
    real_motor_params = {
        'K': 3.2,
        'tau_e': 0.005,
        'tau_m': 0.25,
        'J': 0.02,
        'b': 0.08
    }
    
    real_motor = DCMotorAnalyzer(real_motor_params)
    
    # Generate "experimental" data with realistic characteristics
    time_exp, voltage_exp, speed_exp, true_speed = real_motor.generate_synthetic_data(
        test_type='custom', noise_level=0.05, duration=3.0)
    
    # Add some measurement delays and filtering effects (realistic)
    # Simple low-pass filter to simulate sensor dynamics
    from scipy.signal import butter, filtfilt
    b, a = butter(3, 0.3, 'low')  # 3rd order Butterworth filter
    speed_filtered = filtfilt(b, a, speed_exp)
    
    # Analysis workflow
    print("📋 EXPERIMENTAL DATA ANALYSIS WORKFLOW:")
    print("1. Data Collection and Preprocessing")
    print("2. System Identification")
    print("3. Model Validation")
    print("4. Performance Assessment")
    
    # Step 1: Visualize raw data
    plt.figure(figsize=(15, 8))
    
    plt.subplot(2, 3, 1)
    plt.plot(time_exp, voltage_exp, 'g-', linewidth=2)
    plt.title('Input Voltage')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.grid(True)
    
    plt.subplot(2, 3, 2)
    plt.plot(time_exp, speed_exp, 'b-', alpha=0.7, label='Raw Data')
    plt.plot(time_exp, speed_filtered, 'r-', linewidth=2, label='Filtered')
    plt.title('Motor Speed Measurement')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed')
    plt.legend()
    plt.grid(True)
    
    # Step 2: System identification on filtered data
    identified_real = real_motor.system_identification_from_data(
        time_exp, voltage_exp, speed_filtered, plot=False)
    
    # Step 3: Model validation
    if identified_real:
        # Create identified transfer function
        K_id = identified_real['K']
        tau_id = identified_real['tau']
        tf_identified = ct.TransferFunction([K_id], [tau_id, 1])
        
        # Generate model prediction
        t_model, y_model, _ = ct.forced_response(tf_identified, time_exp, voltage_exp)
        
        plt.subplot(2, 3, 3)
        plt.plot(time_exp, speed_filtered, 'b-', linewidth=2, label='Experimental')
        plt.plot(t_model, y_model, 'r--', linewidth=2, label='Model Prediction')
        plt.title('Model Validation')
        plt.xlabel('Time (s)')
        plt.ylabel('Speed')
        plt.legend()
        plt.grid(True)
        
        # Step 4: Performance assessment
        plt.subplot(2, 3, 4)
        error = speed_filtered - np.interp(time_exp, t_model, y_model)
        plt.plot(time_exp, error, 'r-', linewidth=1)
        plt.title('Model Error')
        plt.xlabel('Time (s)')
        plt.ylabel('Error')
        plt.grid(True)
        
        # Performance metrics comparison
        plt.subplot(2, 3, 5)
        comparison_text = f"""
        PARAMETER COMPARISON:
        ━━━━━━━━━━━━━━━━━━━━━━━━━
        True K:   {real_motor_params['K']:.2f}
        ID K:     {K_id:.2f}
        Error:    {abs(real_motor_params['K'] - K_id):.2f}
        
        True τ:   {real_motor_params['tau_m']:.3f}
        ID τ:     {tau_id:.3f}
        Error:    {abs(real_motor_params['tau_m'] - tau_id):.3f}
        
        MODEL QUALITY:
        ━━━━━━━━━━━━━━━━━━━━━━━━━
        R² Fit:   {identified_real['fit_quality']:.3f}
        RMS Error: {np.sqrt(np.mean(error**2)):.3f}
        """
        
        plt.text(0.05, 0.95, comparison_text, transform=plt.gca().transAxes,
                fontfamily='monospace', fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        plt.axis('off')
        
        # Design recommendations
        plt.subplot(2, 3, 6)
        recommendations_text = f"""
        CONTROL DESIGN RECOMMENDATIONS:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        CURRENT PERFORMANCE:
        • Settling Time: ~{4*tau_id:.1f} s
        • Time Constant: {tau_id:.3f} s
        • Steady-state Gain: {K_id:.1f}
        
        FOR FASTER RESPONSE:
        • Increase controller gain
        • Add derivative action
        • Reduce load inertia
        
        FOR BETTER STABILITY:
        • Add integral action for zero SS error
        • Use lead compensation
        • Consider feed-forward control
        
        NEXT STEPS:
        • Design PID controller
        • Simulate closed-loop performance
        • Implement and test
        """
        
        plt.text(0.05, 0.95, recommendations_text, transform=plt.gca().transAxes,
                fontfamily='monospace', fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        plt.axis('off')
    
    plt.suptitle('Complete DC Motor Analysis Workflow', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def main():
    """Main demonstration function"""
    
    print("🎯 STEP AND IMPULSE RESPONSE ANALYSIS FOR DC MOTOR CONTROL")
    print("=" * 70)
    print("Learning Objectives:")
    print("✓ Understand step and impulse responses")
    print("✓ Extract performance metrics from responses")
    print("✓ Identify system parameters from experimental data")
    print("✓ Apply knowledge to DC motor control")
    print("✓ Complete analysis workflow for real systems")
    print("=" * 70)
    
    # Run practical examples
    practical_dc_motor_examples()
    
    print("\n🎓 LEARNING SUMMARY")
    print("=" * 70)
    print("✅ SKILLS DEVELOPED:")
    print("   • Step and impulse response analysis")
    print("   • Performance metrics calculation")
    print("   • System identification from data")
    print("   • Model validation techniques")
    print("   • Practical motor control applications")
    
    print("\n✅ READY FOR:")
    print("   • PID controller design")
    print("   • Closed-loop system analysis")
    print("   • Advanced controller strategies")
    print("   • Real-time implementation")
    
    print("\n📚 KEY TAKEAWAYS:")
    print("   • Step response reveals system characteristics")
    print("   • Time constants determine response speed")
    print("   • Real data requires filtering and validation")
    print("   • Model quality affects controller performance")
    print("   • Trade-offs exist between speed and stability")
    print("=" * 70)

if __name__ == "__main__":
    main()