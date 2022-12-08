#include <iostream>
#include <vector>
#include <cmath>
#include <stdexcept>

#include "matplotlibcpp.h"
#include "Numcpp_light.hpp"

namespace plt = matplotlibcpp;

class Control{
    private:
        // defined private parametres which is used in calculation
        std::vector<float> alpha {0.0, 0.0};
        std::vector<float> d {0.0, 0.0};
        std::vector<float> theta {0.0, 0.0};
        std::vector<float> p {0,0};
        std::vector<std::vector<float>> s_point {{0.0}, {0.0}};
        std::vector<std::vector<float>> e_point {{0.0}, {0.0}};
        
        double Tn_theta[4][4] = {  
            {1, 0, 0, 0} ,
            {0, 1, 0, 0} ,
            {0, 0, 1, 0} ,
            {0, 0, 0, 1} ,
        };
        
        // Private method:
        // input: swit = switch, choose witch approach of calculation to use, size = size of states, this is used in DH
        //  return: 
        // Note: Forward kinematics refers to the use of the kinematic equations of a robot to compute 
        // the position of the end-effector from specified values for the joint parameters.
        void forward_kinematics(int swit, int size = 0){
            switch (swit){
            case 0:
                fast_calc_fk();
                break;
            case 1:
                DH_calc_fk(size);
            default:
                throw std::runtime_error("[INFO] Don't exists option of calculation of FK!");
                break;
            }
        }
        
        // Private method:
        // input:
        //  return:
        // "Fast" approach of calculating FK, by defined SCARA problem.
        void fast_calc_fk(){
            p[0] = a[0] * cos(theta[0]) + a[1] * cos(theta[0] + theta[1]);
            p[1] = a[0] * sin(theta[0]) + a[1] * sin(theta[0] + theta[1]);
            
            // output
            // cout << p[0] << endl;
            // cout << p[1] << endl;
        };
        
        // Private method:
        // input:
        //  return:
        // Slower, but more modular approach of calculating FK.
        void DH_calc_fk(int len){
            double res[4][4] = {  
                {1, 0, 0, 0} ,
                {0, 1, 0, 0} ,
                {0, 0, 1, 0} ,
                {0, 0, 0, 1} ,
            };

            double Ai_aux[4][4] = {
                {1, 0, 0, 0} ,
                {0, 1, 0, 0} ,
                {0, 0, 1, 0} ,
                {0, 0, 0, 1} ,
            };

            for(int i = 0; i < len; i++){
                Ai_aux[0][0] = cos(theta[i]);
                Ai_aux[0][1] = (-1) * sin(theta[i] * cos(alpha[i]));
                Ai_aux[0][2] = sin(theta[i]) * sin(alpha[i]);
                Ai_aux[0][3] = a[i] * cos(theta[i]);

                Ai_aux[1][0] = sin(theta[i]);
                Ai_aux[1][1] = cos(theta[i]) * cos(alpha[i]);
                Ai_aux[1][2] = (-1) * cos(theta[i]) * sin(alpha[i]);
                Ai_aux[1][3] = a[i] * sin(theta[i]);

                Ai_aux[2][0] = 0;
                Ai_aux[2][1] = sin(alpha[i]);
                Ai_aux[2][2] = cos(alpha[i]);
                Ai_aux[2][3] = d[i];

                Ai_aux[3][0] = 0;
                Ai_aux[3][1] = 0;
                Ai_aux[3][2] = 0;
                Ai_aux[3][3] = 1;

                for (int i = 0; i < 4 ; i++) {
                    for (int j = 0; j < 4; j++) {
                        for (int k = 0; k < 4; k++)
                            Tn_theta[i][j] += res[i][k] * Ai_aux[k][j];
                    }
                }

            }

            for(int i = 0; i < p.size(); i++){
                p[i] = Tn_theta[i][3];
            };

            // output
            // cout << p[0] << endl;
            // cout << p[1] << endl;
        };
        
        // Private method:
        // input: cfg = configuration
        //  return: 
        // Note: Inverse kinematics is the mathematical process of calculating the variable 
        // joint parameters needed to place the end of a kinematic chain.
        void calc_ik(int cfg){

            // Cosine Theorem Beta
            double cosT_beta_numerator = pow(a[0],2) + pow(p[0],2) + pow(p[1],2) - pow(a[1],2);
            double cosT_beta_denumerator = 2 * a[0] * sqrt( pow(p[0],2) + pow(p[1],2) );

            // Calculation angle of Theta 1,2 (Inverse trigonometric functions):
            // Rule 1: The range of the argument “x” for arccos function is limited from -1 to 1.
            // −1 ≤ x ≤ 1
            // Rule 2: Output of arccos is limited from 0 to π (radian).
            // 0 ≤ y ≤ π
            if(cosT_beta_numerator/cosT_beta_denumerator > 1){
                theta[0] = atan2(p[1], p[0]);
                throw std::runtime_error("[INFO] Error: Out of range!");
            }

            else if(cosT_beta_numerator/cosT_beta_denumerator < -1){
                theta[0] = atan2(p[1], p[0]) - M_PI;
                throw std::runtime_error("[INFO] Error: Out of range!");
            }

            else{
                if (cfg == 0){
                    theta[0] = atan2(p[1], p[0]) - acos(cosT_beta_numerator/cosT_beta_denumerator);
                }

                else{
                    theta[0] = atan2(p[1], p[0]) + acos(cosT_beta_numerator/cosT_beta_denumerator);
                }
            }

            // Cosine Theorem Alha
            double cosT_alpha_numerator = (pow(a[0],2) + pow(a[1],2)) - ((pow(p[0],2) + pow(p[1],2)));
            double cosT_alpha_denumerator = 2 * (a[0] * a[1]);
            
            if(cosT_alpha_numerator/cosT_alpha_denumerator > 1){
                theta[1] = M_PI;
                throw std::runtime_error("[INFO] Error: Out of range!");
            }

            else if(cosT_alpha_numerator/cosT_alpha_denumerator < -1){
                theta[1] = 0.0;
                throw std::runtime_error("[INFO] Error: Out of range!");
            }

            else{
                if (cfg == 0){
                    theta[1] = M_PI - acos(cosT_alpha_numerator/cosT_alpha_denumerator);
                }

                else{
                    theta[1] = acos(cosT_alpha_numerator/cosT_alpha_denumerator) - M_PI;
                }
            }

            // Calculation forward_kinematics for case if we have some out of range situation!
            forward_kinematics(0);

            // output
            // cout << theta[0] << endl;
            // cout << theta[1] << endl;
        };

        void plot_envelop(){
            std::vector<std::vector<float>> mesh {{0.0}, {0.0}};

            std::vector<double> theta_1(100);
            theta_1 = meshgen::linspace((ax_wr[0][0]) *  M_PI / 180, (ax_wr[0][1]) *  M_PI / 180, 100);
            
            std::vector<double> theta_2(100);
            theta_2 = meshgen::linspace((ax_wr[1][0]) *  M_PI / 180, (ax_wr[1][1]) *  M_PI / 180, 100);

            meshgen::mesh_grid<double, 0, 2> T1;
            meshgen::mesh_grid<double, 1, 2> T2;
            std::tie(T1, T2) = meshgen::meshgrid(theta_1, theta_2);

            for (size_t i = 0; i < T1.size(); i++){
                for (size_t j = 0; j < T2.size(); j++){
                    mesh[0].push_back(a[0] * cos(T1(i, j)) + a[1] * cos(T1(i, j) + T2(i, j)));
                    mesh[1].push_back(a[0] * sin(T1(i, j)) + a[1] * sin(T1(i, j) + T2(i, j)));
                }
            }

            plt::scatter(mesh[0], mesh[1]);
        }

        void plot_endstart_points(){
            plt::plot(s_point[0], s_point[1],    {{"color", "darkred"},{"marker", "o"},{"ms","10"},{"label","Start point"}});
            plt::plot(e_point[0], e_point[1],    {{"color", "darkgreen"},{"marker", "o"},{"ms","10"},{"label","End point"}});
        }
        
        // Private method:
        // input:
        //  return: 
        // Note: Plotting method, just set bounderies, specified base, joint,
        // end-effector, and links betwwen them. Simple approach how to use
        // C-Matplotlib. 
        void plot_env(){            
            float axis_max = ((1)*(a[0] + a[1]) + 0.2);
            float axis_min = ((-1)*(a[0] + a[1]) - 0.2);
            
            std::vector<float> aux_0 {0.0, a[0] * cos(theta[0])};
            std::vector<float> aux_1 {0.0, a[0] * sin(theta[0])};
            
            std::vector<std::vector<float>> base {{0.0}, {0.0}};
            std::vector<std::vector<float>> joint {{a[0] * cos(theta[0])}, {a[0] * sin(theta[0])}};
            std::vector<std::vector<float>> end_eff {{p[0]}, {p[1]}};
            
            plt::plot(aux_0, aux_1,              {{"color", "black"}, {"linewidth", "10"}});

            aux_0[0] = a[0] * cos(theta[0]);
            aux_0[1] = p[0];
            aux_1[0] = a[0] * sin(theta[0]);
            aux_1[1] = p[1];

            plt::plot(aux_0, aux_1,              {{"color", "black"}, {"linewidth", "10"}});
            plt::plot(base[0], base[1],          {{"color", "gold"},{"marker", "o"},{"ms","20"},{"label","Base"}});
            plt::plot(joint[0], joint[1],        {{"color", "gold"},{"marker", "o"},{"ms","15"},{"label","Joint"}});
            plt::plot(end_eff[0], end_eff[1],    {{"color", "grey"},{"marker", "o"},{"ms","15"},{"label","End-Effector"}});

            plt::grid(true);

            plt::xlim(axis_min, axis_max);
            plt::ylim(axis_min, axis_max);

            plt::xlabel("x position [m]", {{"fontsize","15"}});
            plt::ylabel("y position [m]", {{"fontsize","15"}});
            plt::title("SCARA ROBOT " + robot_name, {{"fontsize","20"}});
            plt::legend({{"loc","upper left"},{"fontsize","20"}});
        };

    public:
        // All specifed public parametres, which is used through alll class
        // importat states, this parametres is used for compute in anim_fk, anim_ik
        std::vector<std::vector<float>> states_fk;
        std::vector<std::vector<float>> states_ik;
        // configuration
        std::vector<float> cfg;

        // axes reach range
        std::vector<std::vector<float>> ax_wr;
        // arm length 
        std::vector<float> a;

        // printing parametres
        std::string robot_name;
        std::string company;
        std::string url_datasheet;

        // Public method:
        // input: swit = switch, decide FK computing method
        //  return: 
        // Note: 1. get private variable for storage previous computed theta parameter,
        // 2. go for loop in size of all inputed fk states, then compute radians from degrees,
        // 3. check if is only 1. state, then static plot show(). 4. compute linspace between new
        // and old state, then compute in loop and show animation. 
        void anim_fk(int swit){            
            std::vector<float> old_theta {0.0,0.0};
            for (int i = 0; i < states_fk.size(); i++){
                for(int k = 0; k < states_fk[i].size(); k++){
                    theta[k] = states_fk[i][k] * M_PI / 180;
                }

                if (states_fk.size() == 1){
                    forward_kinematics(swit);
                    plt::clf();

                    plot_env();
                    plot_envelop();
                    
                    plt::show();
                    break;
                }

                // If u not in 0. state, then compute between new and old state FK.
                if (i != 0){
                    std::vector<double> theta_x = meshgen::linspace(old_theta[0] + 0.0, theta[0] + 0.0, 20);
                    std::vector<double> theta_y = meshgen::linspace(old_theta[1] + 0.0, theta[1] + 0.0, 20);
                    for (int l = 0; l < theta_x.size(); l++){
                        theta[0] = theta_x[l];
                        theta[1] = theta_y[l];
                        forward_kinematics(swit);

                        plt::clf();

                        plot_env();
                        plot_endstart_points();
                        
                        plt::pause(0.01);
                    }
                }

                // plot first state
                else{
                    old_theta[0] = theta[0];
                    old_theta[1] = theta[1];

                    forward_kinematics(swit);

                    s_point[0][0] = p[0];
                    s_point[1][0] = p[1];

                    theta[0] = states_fk.back()[0] * M_PI / 180;
                    theta[1] = states_fk.back()[1] * M_PI / 180;

                    forward_kinematics(swit);
                    
                    e_point[0][0] = p[0];
                    e_point[1][0] = p[1];

                    theta[0] = old_theta[0];
                    theta[1] = old_theta[1];

                    plot_env();
                    plot_endstart_points();
                }

                // get old states
                old_theta[0] = theta[0];
                old_theta[1] = theta[1];
            }
        };

        // Public method:
        // input:
        //  return: 
        // Note: 1. check if states has same size as cfgs. 2. get private variable for storage previous 
        // points. 2. go for loop in size of all inputed ik states.
        // 3. check if is only 1. state, then static plot show(). 4. compute linspace between new
        // and old state, then compute in loop and show animation. 
        void anim_ik(){
            if (states_ik.size() != cfg.size()){
                throw std::runtime_error("[INFO] Check if match cfgs with points!");
            };

            std::vector<float> old_p {0.0, 0.0};
            for (int i = 0; i < states_ik.size(); i++){
                for (int k = 0; k < states_ik[i].size(); k++){
                    p[k] = states_ik[i][k];
                }
                
                if (states_ik.size() == 1){
                    calc_ik(cfg[0]);

                    plt::clf();

                    plot_env();
                    plot_envelop();

                    plt::show();
                    break;
                }
                
                if (i != 0){
                    std::vector<double> p_x = meshgen::linspace(old_p[0] + 0.0, p[0] + 0.0, 20);
                    std::vector<double> p_y = meshgen::linspace(old_p[1] + 0.0, p[1] + 0.0, 20);
                    
                    for (int l = 0; l < p_x.size(); l++){
                        p[0] = p_x[l];
                        p[1] = p_y[l];
                        calc_ik(cfg[l]);
                        
                        plt::clf();

                        plot_env();
                        plot_endstart_points();

                        plt::pause(0.01);
                    }
                }
                else{
                    s_point[0][0] = p[0];
                    s_point[1][0] = p[1];

                    e_point[0][0] = states_ik.back()[0];
                    e_point[1][0] = states_ik.back()[1];

                    plot_env();
                    plot_endstart_points();
                }

                old_p[0] = p[0];
                old_p[1] = p[1];
            }
        };

        // Some simple and basic info printing
        void info(){
            std::cout << "----------------------------------------------------------" << std::endl;
            std::cout << "[INFO] VOB - Project" << std::endl;
            std::cout << "[INFO] Simple Inverse Kinem. and Forward Kinem. calculator" << std::endl;
            std::cout << "[INFO] Author: Martin Juricek" << std::endl;
            std::cout << "[INFO] IACS FME BUT @2021" << std::endl;
            std::cout << "----------------------------------------------------------" << std::endl;
            std::cout << "[INFO] - SCARA robot -" << std::endl;
            std::cout << "[INFO] Company: " << company << std::endl;
            std::cout << "[INFO] Robot: " << robot_name << std::endl;
            std::cout << "[INFO] angular reach axis 1: " << ax_wr[0][1]*2 << "°" << std::endl;
            std::cout << "[INFO] angular reach axis 2: " << ax_wr[1][1]*2 << "°" << std::endl;
            std::cout << "[INFO] Datasheet: " << url_datasheet << std::endl;
            std::cout << "----------------------------------------------------------" << std::endl;
        }
};

int main(){
    // There you can specifed parametres of your desired SCARA robot compute,
    // ax_ws = axis reach range = if you have angular reach, just split, as you can see in info
    // arm lengtg = just look at datasheet
    std::vector<std::vector<float>> ax_wr {{-180.0, 180.0}, {-150.0, 150.0}};
    std::vector<float> arm_length = {0.38, 0.24};

    // Instance of class Control, there is can be specifed some info about SCARA,
    // also importnat is to add axis range [X,Y] + arm length, important for computing
    Control scara;
    scara.company = "Stäubli";
    scara.robot_name = "TS2-60";
    scara.url_datasheet = "https://www.staubli.com/en-sg/file/24130.show";

    scara.ax_wr = ax_wr;
    scara.a = arm_length;

    // Show some info about program etc ... 
    scara.info();

    std::cout << "[INFO] Example numero uno" << std::endl;
    // Example n.1 - show using ik in single static show 
    // So if you don't to see animation, just set only 1 point with 1 conf.
    scara.states_ik.clear();
    scara.cfg.clear();

    scara.states_ik.push_back({0.25, 0.2});
    scara.cfg.push_back({1});

    scara.anim_ik();

    std::cout << "[INFO] Example numero due" << std::endl;
    // Example n.2 - show using ik in loop
    // It is important to feed vector of states and cfgs -> same size
    // So every point needs to specify his configuration! 
    for(int i = 0; i < 1; i++){
        scara.states_ik.clear();
        scara.cfg.clear();
        scara.states_ik.push_back({0.3, 0.15});
        scara.cfg.push_back({0});

        scara.states_ik.push_back({0.5, 0.2});
        scara.cfg.push_back({0});

        scara.anim_ik();
    }
    
    scara.states_fk.clear();
    
    std::cout << "[INFO] Example numero tre" << std::endl;
    // Example n.3 - show using fk in single static show 
    // So if you don't to see animation, just set only 1 point with 1 conf.
    scara.states_fk.push_back({35.0, 90.0});
    scara.anim_fk(0);
    
    scara.states_fk.clear();
    
    std::cout << "[INFO] Example numero quattro" << std::endl;
    // Example n.4 - show non loop animation of FK
    // FK has 2 option of computing:
    // 0 - Fast Forward Kinematics
    // 1 - Denavit - Hartenberg Table
    scara.states_fk.push_back({0.0, 45.0});
    scara.states_fk.push_back({35.0, 90.0});
    scara.anim_fk(0);

    scara.states_fk.clear();
}