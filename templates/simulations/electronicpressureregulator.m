function [response] = main(data)
    %% This is the first function to be called when executing the script
    %  -----------------------------------------------------------------
    %  Data: Scalar structure with data comming from Valispace.
    %
    %  Example of use:
    %       mass = data.mass
    %  ------------------------------------------------------------------
    %  Response: Scalar structure with data to send to Valispace.
    %
    %  Example of use:
    %       response = struct()
    %       response.total_mass = data.mass * 10
    %       response.double_mass = data.mass * 2
    %  ------------------------------------------------------------------

    % Get inputs from Valispace
    P_in = data.P_in;
    V_in = data.V_in;
    
    % Previous code from simulation
    V_in = 1.2 ;  
    F_1 = 25 ; 
    PV_1 = P_in*V_in;
    m_dot = 6; 
    density = 5.761; 
    A_inlet = m_dot / (density*V_in);
    A_2 = A_inlet/2.5;
    m_dot2 = 5;
    V_2 = m_dot2/(density*A_2);
    P_2 = PV_1/V_2; 
    A_orifice = F_1/P_2; 
    PV_2 = P_2*V_2; 
    V_out = 70.58882;
    Pout = PV_2/V_out;

    % Send outputs back to Valispace
    response = struct()
    response.Pout = Pout;
    
end
