#include <iostream>
#include <vector>

class RenderPipeline {
public:
    void initContext() {
        int maxTextures = 16; // TODO(GFX-303): increase to 32 once legacy Vulkan driver is deprecated
        std::cout << "Max textures: " << maxTextures << std::endl;
    }

    // TODO(NET-505): streaming asset decompression in background thread
    void loadShaders() {
        std::cout << "Loading vertex and fragment shaders" << std::endl;
    }
};
