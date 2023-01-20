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
    g = data.g;
    SIGMA = data.SIGMA;
    
    % Previous code from simulation
    k = 1e-5; %initial guess
    Gamma = sqrt(g)*(2/(g+1))^((g+1)/(2*g-2));
    a = 2*g/(g-1);
    b = 2/g;
    c = (g+1)/g;
    f = Gamma/sqrt(a*(k^b-k^c)) - SIGMA; %f(x)
    df = a*(c*Gamma*k^c-b*Gamma*k^b)/(2*k*(a*(k^b-k^c))^(3/2)); %f&#x27;(x)
    k_next = k-f/df; %Next guess
    difference = abs(k_next-k)/k;
    counter = 0;
    
    while difference &gt; k*1e-2
    
        k = k_next;
        f = Gamma/sqrt(a*(k^b-k^c)) - SIGMA; %f(x)
    
        df = a*(c*Gamma*k^c-b*Gamma*k^b)/(2*k*(a*(k^b-k^c))^(3/2)); %f&#x27;(x)
        k_next = k-f/df;%Next guess
        difference = abs(k_next-k);
        counter = counter + 1;
    
    endwhile
    
    C_F = Gamma*sqrt(a*(1-k^((g-1)/g)))+SIGMA*(k);
    k = k_next;

    % Send outputs back to Valispace
    response = struct()
    response.C_F = C_F;
    response.k = k;
    
end
    