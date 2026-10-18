function inspectLeafClearance(root) {
    const fs = require('fs');
    const crypto = require('crypto');
    const results = [];
    const uvErrors = [];
    const assetHashes = {};
    for (const age of [6, 7]) {
        for (let variation = 0; variation < 4; variation++) {
            const modelName = 'wheat_stage' + age + (variation ? '_variant' + variation : '');
            ModelProject.all.filter(p => p.name === modelName && p.save_path).at(-1).select();
            scene.updateMatrixWorld(true);
            const pixels = new Map(Texture.all.map(t => [t.id, {width: t.width, height: t.height, data: t.canvas.getContext('2d').getImageData(0, 0, t.width, t.height).data}]));
            const triangles = cube => {
                const g = cube.mesh.geometry;
                const vertices = g.attributes.position;
                const uv = g.attributes.uv;
                const list = [];
                for (let i = 0; i < g.index.count; i += 3) {
                    const indices = [0, 1, 2].map(j => g.index.getX(i + j));
                    const points = indices.map(j => new THREE.Vector3().fromBufferAttribute(vertices, j).applyMatrix4(cube.mesh.matrixWorld));
                    list.push({shape: new THREE.Triangle(...points), uv: indices.map(j => new THREE.Vector2().fromBufferAttribute(uv, j))});
                }
                return list;
            };
            const opaque = (triangle, point, texture) => {
                const bary = triangle.shape.getBarycoord(point, new THREE.Vector3());
                const uv = triangle.uv[0].clone().multiplyScalar(bary.x).addScaledVector(triangle.uv[1], bary.y).addScaledVector(triangle.uv[2], bary.z);
                const bitmap = pixels.get(texture);
                const x = Math.min(bitmap.width - 1, Math.max(0, Math.floor(uv.x * bitmap.width)));
                const y = Math.min(bitmap.height - 1, Math.max(0, Math.floor((1 - uv.y) * bitmap.height)));
                return bitmap.data[(y * bitmap.width + x) * 4 + 3] === 255;
            };
            const crosses = (first, second, textureA, textureB, attachment) => {
                for (const a of first) for (const b of second) {
                    const plane = new THREE.Plane().setFromCoplanarPoints(b.shape.a, b.shape.b, b.shape.c);
                    const corners = [a.shape.a, a.shape.b, a.shape.c];
                    const hits = [];
                    for (let edge = 0; edge < 3; edge++) {
                        const start = corners[edge], end = corners[(edge + 1) % 3];
                        const d0 = plane.distanceToPoint(start), d1 = plane.distanceToPoint(end);
                        if (d0 * d1 < 0) hits.push(start.clone().lerp(end, d0 / (d0 - d1)));
                    }
                    if (hits.length !== 2) continue;
                    const steps = Math.max(2, Math.ceil(hits[0].distanceTo(hits[1]) / 0.025));
                    for (let i = 0; i <= steps; i++) {
                        const p = hits[0].clone().lerp(hits[1], i / steps);
                        if (attachment && p.distanceTo(attachment) < 0.8) continue;
                        if (b.shape.containsPoint(p) && opaque(a, p, textureA) && opaque(b, p, textureB)) return true;
                    }
                }
                return false;
            };
            const plants = Cube.all.slice(0, 4).map(c => ({name: c.name, triangles: triangles(c)}));
            const leaves = Cube.all.slice(4).map(c => ({name: c.name, triangles: triangles(c), root: Cube.all.find(b => b.name === c.name.replace(/_(base|tip)$/, '_base')).mesh.getWorldPosition(new THREE.Vector3())}));
            for (const cube of Cube.all.slice(4)) {
                const geometry = cube.mesh.geometry;
                for (let i = 8; i < 12; i++) {
                    const position = new THREE.Vector3().fromBufferAttribute(geometry.attributes.position, i);
                    const uv = new THREE.Vector2().fromBufferAttribute(geometry.attributes.uv, i);
                    const opposite = [12, 13, 14, 15].find(j => {
                        const other = new THREE.Vector3().fromBufferAttribute(geometry.attributes.position, j);
                        return Math.abs(position.x - other.x) < 0.0001 && Math.abs(position.z - other.z) < 0.0001;
                    });
                    const otherUv = new THREE.Vector2().fromBufferAttribute(geometry.attributes.uv, opposite);
                    if (uv.distanceTo(otherUv) > 0.0001) uvErrors.push({age, leaf: cube.name, reason: 'Upper and lower surfaces disagree'});
                }
                if (!cube.name.endsWith('_base')) continue;
                const tip = Cube.all.find(c => c.name === cube.name.replace(/_base$/, '_tip'));
                let matchingCorners = 0;
                for (let i = 8; i < 12; i++) for (let j = 8; j < 12; j++) {
                    const a = new THREE.Vector3().fromBufferAttribute(geometry.attributes.position, i).applyMatrix4(cube.mesh.matrixWorld);
                    const b = new THREE.Vector3().fromBufferAttribute(tip.mesh.geometry.attributes.position, j).applyMatrix4(tip.mesh.matrixWorld);
                    if (a.distanceTo(b) > 0.005) continue;
                    matchingCorners++;
                    const uvA = new THREE.Vector2().fromBufferAttribute(geometry.attributes.uv, i);
                    const uvB = new THREE.Vector2().fromBufferAttribute(tip.mesh.geometry.attributes.uv, j);
                    if (uvA.distanceTo(uvB) > 0.0001) uvErrors.push({age, leaf: cube.name, reason: 'UV discontinuity at bend'});
                }
                if (matchingCorners !== 2) uvErrors.push({age, leaf: cube.name, reason: 'Missing two shared bend corners'});
            }
            const assets = ['models/block/' + modelName + '.json'].concat(Texture.all.map(t => 'textures/block/' + t.name));
            for (const asset of assets) {
                const path = 'common/src/main/resources/assets/farmerplus/' + asset;
                assetHashes[path] = crypto.createHash('sha256').update(fs.readFileSync(root + '/' + path)).digest('hex');
            }
            const collisions = [];
            for (const leaf of leaves) for (let index = 0; index < plants.length; index++) {
                const plant = plants[index];
                const texture = index === 0 || index === 3 ? 'crop' : 'alternate';
                if (crosses(leaf.triangles, plant.triangles, 'foliage', texture, leaf.root)) collisions.push([leaf.name, plant.name]);
            }
            for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) {
                if (leaves[i].name.replace(/_(base|tip)$/, '') === leaves[j].name.replace(/_(base|tip)$/, '')) continue;
                if (crosses(leaves[i].triangles, leaves[j].triangles, 'foliage', 'foliage')) collisions.push([leaves[i].name, leaves[j].name]);
            }
            results.push({age, variation, collisions});
        }
    }
    const report = {method: 'Blockbench mesh triangle intersections sampled every 0.025 model units with actual texture alpha; first 0.8 units around each leaf attachment excluded', scope: 'Four exported height-and-texture models per age, AGE 6 and 7. Screen-space occlusion and neighbouring crop overlap are not geometric clipping measurements.', uvErrors, assetHashes, results};
    fs.mkdirSync(root + '/build/art/validation', {recursive: true});
    fs.writeFileSync(root + '/build/art/validation/leaf-clearance.json', JSON.stringify(report, null, 2) + '\n');
    return report;
}
