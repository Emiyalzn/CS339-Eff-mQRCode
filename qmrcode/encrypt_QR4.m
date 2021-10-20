%% ==========================================
%% Encrypt QR code using Phase Modulation (Ubicomp Poster 2018)
%%
%% Try different distans and angles in this version.
%% 
%% CFA: m_1(x, y) = p_1(phi_1(x, y))
%%   p_1(u) = mod(round(phase), 2): square function
%%   phi_1(x, y) = x + y
%%
%% Camouflaging Pattern: m_2(x, y) = p_2(phi_2(x, y))
%%   p_2(u) = mod(round(phase), 2): square function
%%   phi_2(x, y) = x + y    ,  for black pixels
%%   phi_2(x, y) = x + y + 1,  for white pixels
%%   
%% ==========================================

function encrypt_QR4()

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Read QR code image
    filename = 'mbc19_qrcode.jpg';
    I = imread(filename);

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% up-sampling (make image larger) and using only black white
    nrows = size(I, 1);
    ncols = size(I, 2);
    ratio = 2;
    I2 = zeros(nrows*ratio, ncols*ratio);
    for xi = 1:nrows
        for yi = 1:ncols
            I2((xi-1)*ratio+1:xi*ratio, (yi-1)*ratio+1:yi*ratio) = I(xi, yi, 1);
        end
    end
    I2 = imresize(I(:,:,1), ratio);
    I = double(I2) / 255;
    nrows = size(I, 1);
    ncols = size(I, 2);
    fprintf('  up-sampling = %dx%d\n', size(I));
    
    fh = figure(1); clf;
    imshow(I);
    truesize(fh);
    title('original image');
    pause(0.01)


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Encode QR code with Moire pattern
    Iencode = zeros(size(I));
    %Iencode2 = zeros(size(I2));
    for xi = 1:nrows
        for yi = 1:ncols
            %% make sure block and white are in different phases
            if I(xi, yi) > 0.5
                Iencode(xi, yi)  = p_g1_func(phi_g1_func(xi, yi));
                %Iencode2(xi, yi) = p_g1_func(phi_g2_func(xi, yi));
            else
                Iencode(xi, yi)  = p_g1_func(phi_g1_func(xi, yi)+1);
                %Iencode2(xi, yi) = p_g1_func(phi_g2_func(xi, yi)+1);
            end
        end
    end

    fh = figure(2); clf;
    I2 = zeros(nrows, ncols, 3);
    I2(:,:,2) = Iencode;
    imshow(Iencode);
    % imshow(I2);
    truesize(fh);
    title('Iencode');
    pause(0.01)


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Add Fake Boundary for Camouflage 
    Ifake = addFakeBoundary(Iencode, 200);

    fh = figure(3); clf;
    imshow(Ifake);
    truesize(fh);
    title('fake boundary');
    pause(0.01)


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Add white noise
    Inoise = addWhiteNoise(Iencode, 0.1);
    
    %% Leave the three locator
    %top left
    Inoise(1:7*10*ratio, 1:7*10*ratio) = I(1:7*10*ratio, 1:7*10*ratio);
    %top right
    Inoise(1:7*10*ratio, 22*10*ratio:29*10*ratio) = I(1:7*10*ratio, 22*10*ratio:29*10*ratio);
    %left bottom
    Inoise(22*10*ratio:29*10*ratio, 1:7*10*ratio) = I(22*10*ratio:29*10*ratio, 1:7*10*ratio);
    
    fh = figure(4); clf;
    imshow(Inoise);
    imwrite(Inoise,'test.png');
    truesize(fh);
    %title('noise');
    pause(0.01)


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Simulation: superposition with camera
    %Icamera = simCameraLayer(nrows, ncols);
    %Idec = Inoise .* Icamera;

    %fh = figure(5); clf;
    %imshow(Icamera);
    %truesize(fh);
    %title('camera');
    %pause(0.01)

    %fh = figure(6); clf;
    %imshow(Idec);
    %truesize(fh);
    %title('simulation');
    %pause(0.01)
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Periodic Functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Green Pixels
function m = p_g1_func(phase)
    m = mod(round(phase), 2);
end

%% Red Pixels
function m = p_r1_func(phase)
    m = phase;
end

%% cos
function m = p1_func(phase)
    m = 1/2 + 1/2 * cos(phase*2);
end

%% exp
function m = p2_func(phase)
    m = exp(2*abs(1-mod(phase/pi,2)))/exp(2);
end

%% log
function m = p3_func(phase)
    m = log(1+3*abs(1-mod(phase/pi,2)))/log(4);
end

%% square
function m = p4_func(phase)
    m = round(mod(phase/2/pi,1)); 
end

%% triangle
function m = p5_func(phase)
    m = abs(1-mod(phase/pi,2));
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Phase Functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Green Pixels 1
function phase = phi_g1_func(x, y)
    phase = x + y;
end

%% Green Pixels 2
function phase = phi_g2_func(x, y)
    phase = floor((x-1)/2) + floor((y-1)/2);
end

%% Red Pixels 1
function phase = phi_r1_func(x, y)
    if mod(x, 2) == 1 & mod(y, 2) == 0
        phase = 1;
    else
        phase = 0;
    end
end

%% Red Pixels 2
function phase = phi_r2_func(x, y)
    if mod(x, 2) == 0 & mod(y, 2) == 1
        phase = 1;
    else
        phase = 0;
    end
end

%% horizontal lines
function phase = phi1_func(x, y)
    phase = x;
end

%% vertical lines
function phase = phi2_func(x, y)
    phase = y;
end





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% compute inverse pm
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function phase = pm_inverse(pm_x, pm, y)
    [~,idx] = min(abs(pm-y));
    idx = idx(1);

    %% interplation
    if idx == 1 | idx == length(pm_x)
        phase = pm_x(idx);
    else
        xx = pm_x([idx-1:idx+1]);
        yy = pm([idx-1:idx+1]);
        phase = interp1(yy, xx, y);
    end
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Functions to blur boundary
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Add Fake Boundary for Camouflage 
%% @INPUT(Iencode): encoded QR code image
%% @INPUT(thr): the minimal distance between fake boundary (unit: pixel) 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Ifake] = addFakeBoundary(Iencode, thr)
    Ifake = Iencode;
    nrows = size(Iencode, 1);
    ncols = size(Iencode, 2);
    fake_rows = [];
    fake_cols = [];

    for xi = 1:nrows-1
        for yi = 1:ncols-1
            if Iencode(xi, yi) == Iencode(xi, yi+1)
                %% Find a col with boundary
                if_gen_fake_col = 1;
                if length(fake_cols) > 0
                    if min(abs(fake_cols - yi)) < thr
                        if_gen_fake_col = 0;
                    end
                end

                %% Start to generate fake boundary
                if if_gen_fake_col == 1
                    for xj = 1:nrows
                        Ifake(xj, yi+1) = Ifake(xj, yi);
                    end
                    fake_cols = [fake_cols, yi];
                end
            end

            if Iencode(xi, yi) == Iencode(xi+1, yi)
                %% Find a row with boundary
                if_gen_fake_row = 1;
                if length(fake_rows) > 0
                    if min(abs(fake_rows - xi)) < thr
                        if_gen_fake_row = 0;
                    end
                end

                %% Start to generate fake boundary
                if if_gen_fake_row == 1
                    for yj = 1:ncols
                        Ifake(xi+1, yj) = Ifake(xi, yj);
                    end
                    fake_rows = [fake_rows, xi];
                end
            end

        end
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Add White Noise
%% @INPUT(Iencode): encoded QR code image
%% @INPUT(ratio): ratio of noise
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Inoise] = addWhiteNoise(Iencode, ratio)
    Inoise = Iencode;
    nrows = size(Iencode, 1);
    ncols = size(Iencode, 2);
    fake_rows = [];
    fake_cols = [];

    noise = rand(nrows, ncols);
    idx = find(noise <= ratio);
    
    idx1 = find(Inoise(idx) > 0.5);
    Inoise(idx(idx1)) = 0;

    idx2 = find(Inoise(idx) > 0.5);
    Inoise(idx(idx2)) = 1;
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Blur Boundary
%% @INPUT(Iencode): encoded QR code image
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Inoise] = addBlurBoundary(Iencode)
    Iblur = Iencode;
    %% XXX: todo
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% simulate the camera layer
%% @INPUT(w): width of the camera
%% @INPUT(h): height of the camera
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Icamera] = simCameraLayer(h, w)
    Icamera = zeros(h, w);
    for xi = 1:h
        for yi = 1:w
            % if (mod(xi, 4) == 0 | mod(xi, 4) == 1) & ...
            %    (mod(yi, 4) == 0 | mod(yi, 4) == 1)
            %     Icamera(xi, yi) = 1;
            % elseif (mod(xi, 4) == 0 | mod(xi, 4) == 1) & ...
            %    (mod(yi, 4) == 2 | mod(yi, 4) == 3)
            %     Icamera(xi, yi) = 0;
            % elseif (mod(xi, 4) == 2 | mod(xi, 4) == 3) & ...
            %    (mod(yi, 4) == 0 | mod(yi, 4) == 1)
            %     Icamera(xi, yi) = 0;
            % else
            %     Icamera(xi, yi) = 1;
            % end
            if (mod(xi, 3) == 0 | mod(xi, 3) == 1) & ...
               (mod(yi, 3) == 0 | mod(yi, 3) == 1)
                Icamera(xi, yi) = 1;
            elseif (mod(xi, 3) == 0 | mod(xi, 3) == 1) & ...
               (mod(yi, 3) == 2)
                Icamera(xi, yi) = 0;
            elseif (mod(xi, 3) == 2) & ...
               (mod(yi, 3) == 0 | mod(yi, 3) == 1)
                Icamera(xi, yi) = 0;
            else
                Icamera(xi, yi) = 1;
            end
        end
    end
end


function checkRedPixels()
    nrows = 900;
    ncols = 900;
    I = zeros(nrows, ncols);
    for x = 1:nrows
        for y = 1:ncols
            if (x < nrows/2 & y < ncols/2) | (x >= nrows/2 & y >= ncols/2)
                I(x, y) = p_r1_func(phi_r1_func(x,y));
            else
                % I(x, y) = p_r1_func(phi_r2_func(x,y));
                I(x, y) = p_g1_func(phi_g1_func(x,y));
            end
        end
    end

    fh = figure(11); clf;
    imshow(I);
    truesize(fh);
    title('sim red pixels');
end