function [centerX, centerY] = seedStrain(image, man_res, option)

    % SUMMARY: Seed Point generation alogorithm for breast ultrasound image
    % based on domain knowledge

    % Steps:
    % 1. SRAD Filtering 2. CLACHE Imaging 3. Pre-processing by Madabhusi / PMO
    % 4. Othsu's Thresholding and morphological operations 5. Seed Gen 
    % 6. Ranking 7. Seed Point Gen 8. Refining seed point by bwselect (Optional)
    % 9. Seed Point Display optional

    % Input: - image: Original Image
    %        - man_res: Manual Trace Image
    %        - Display option: 1: Show seed ; 0: Dont show seed
    % Output: - centerX: row co-ordinate of seed point
    %         - centerY: column co-ordinate of seed point
    %% Preprocessing Block

    % Joint Probability Image Formation
    [joint] = joint_prob_im(image);

    % Entropy Filtering 
    circularStructure = strel('disk', 8, 8);   % Creating Circular Stucture
    nhood = getnhood(circularStructure);       % Creating Neighbourhood 
    entropyFiltered = entropyfilt(image,nhood);   % Entropy Filtering

    %% Binary Thresholding Block

    imageNegative = 1 - im2double(image);

    circularStructure = strel('disk', 12);

    % Binary SRAD CLACHE Image

    grayThreshold = graythresh(imageNegative);
    
    binarizedImage = imopen(imageNegative, circularStructure);
    binarizedImage = imbinarize(binarizedImage, grayThreshold);

    % Final Binary Image

    %% Post Processing Block

    isolatedLesion = bwareaopen(binarizedImage, 14000);  % Removing area with < 550px

    %% Calculating features for energy function

    [labeledImage, ~] = bwlabel(isolatedLesion ~= 0);
    measurements = regionprops(labeledImage,'Centroid');
    allCentroids = [measurements.Centroid];
    xCentroids = allCentroids(1:2:end);     % Column coordinate for candidate seeds
    yCentroids = allCentroids(2:2:end);     % Row coordinate for candidate seeds

    % Creating Seed Points Possibilities

    xCentroids = round(xCentroids);          
    yCentroids = round(yCentroids);

    [rmax, cmax]=size(joint);
    k1 = 1; k2 = 5;
    for image = 1:length(xCentroids)
        current_row = yCentroids(image);
        
        if current_row + 10 > rmax
            new_row = [yCentroids(image), yCentroids(image) - 10, yCentroids(image), rmax];
        elseif yCentroids(image) - 10 < 1
            new_row = [yCentroids(image), 1, yCentroids(image), yCentroids(image) + 10];
        else
            new_row = [yCentroids(image), yCentroids(image) - 10, yCentroids(image), yCentroids(image) + 10];
        end
        
        if xCentroids(image) + 10 > cmax
            new_col = [xCentroids(image) - 10, xCentroids(image), cmax, xCentroids(image)];
        elseif xCentroids(image) - 10 < 1 
            new_col = [1, xCentroids(image), xCentroids(image) + 10, xCentroids(image)];
        else
            new_col = [xCentroids(image) - 10, xCentroids(image), xCentroids(image) + 10, xCentroids(image)];
        end
        
        row_can_seed(k1:k2)=[yCentroids(image) new_row];
        col_can_seed(k1:k2)=[xCentroids(image) new_col];
        k1 = k1 + 5;
        k2 = k2 + 5;
    end

    % Refining Candidate Seeds
    
    for p = 1:length(row_can_seed)

        if row_can_seed(p) > rmax
            row_can_seed(p) = rmax;
        end

        if col_can_seed(p) > cmax
            col_can_seed(p) = cmax;
        end

        plot(col_can_seed(p), row_can_seed(p), 'g*');
    end

    % Image Center Determination

    Dum_Im = ones(size(isolatedLesion));
    [labIm, ~] = bwlabel(Dum_Im ~= 0);
    meas = regionprops(labIm,'Centroid');
    cen = [meas.Centroid];  % Center
    imX = round(cen(1, 1));  % Column 
    [pr, ~] = size(isolatedLesion);
    imY = round(pr/3); % Row

    for image = 1:length(row_can_seed)
        eu_dis = Distance(row_can_seed(image), col_can_seed(image), imY, imX);
        joint_value = joint(row_can_seed(image), col_can_seed(image));                 % Joint Probabilty @ current seed
        [xgrid, ygrid] = meshgrid(1:size(joint, 2), 1:size(joint, 1));
        mask = ((xgrid - col_can_seed(image)).^2 + (ygrid-row_can_seed(image)).^2) <= 20.^2;
        values = joint(mask);
        total = sum(sum(values));
        av = total;
        av1 = entropyFiltered(row_can_seed(image), col_can_seed(image)); % Entropy @ seed point  
        val(image)=(av*joint_value)./(eu_dis*av1);
    end

    seed = find(val == max(val));
    r_seed = row_can_seed(seed);
    c_seed = col_can_seed(seed);

    %% Displaying seed point atop original image.
    offset1 = 0;
    centerX = r_seed(1);
    centerY = c_seed(1)+offset1;

end