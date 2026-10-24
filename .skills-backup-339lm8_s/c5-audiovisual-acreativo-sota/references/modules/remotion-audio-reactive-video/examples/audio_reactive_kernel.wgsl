// audio_reactive_kernel.wgsl
// Kernel de Cómputo WebGPU para Apple Silicon (M3 Pro Metal Backend)
// Transduce el campo acústico a 100.000 partículas en espacio tridimensional

struct Particle {
    pos: vec3<f32>,
    vel: vec3<f32>,
    color: vec4<f32>,
    life: f32,
};

struct AudioUniforms {
    subBass: f32,
    bass: f32,
    mids: f32,
    highs: f32,
    onset: f32,
    time: f32,
};

@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
@group(0) @binding(1) var<uniform> audio: AudioUniforms;

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let idx = id.x;
    if (idx >= arrayLength(&particles)) {
        return;
    }

    var p = particles[idx];

    // Fuerza radial impulsada por Sub-Bass y Onset percusivo
    let dist = length(p.pos);
    let dir = normalize(p.pos);
    
    // Deformación del campo por armónicos
    let wave = sin(dist * 8.0 - audio.time * 4.0 + audio.mids * 10.0);
    let force = dir * (audio.subBass * 2.5 + audio.onset * 5.0) * wave;

    p.vel = p.vel * 0.94 + force * 0.05;
    p.pos = p.pos + p.vel;

    // Modulación cromática por frecuencias agudas
    p.color = vec4<f32>(
        0.2 + audio.subBass * 0.8,
        0.4 + audio.mids * 0.6,
        0.8 + audio.highs * 0.2,
        0.8 * (1.0 - (dist / 10.0))
    );

    particles[idx] = p;
}
