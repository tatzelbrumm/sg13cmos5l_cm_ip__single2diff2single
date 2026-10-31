# writes the C(V) control block into a deck: devices hang on sources V<name>, areas in um2
import sys
deck, = sys.argv[1:2]
body = open(deck).read().split('.control')[0]
srcs = [l.split()[0][1:] for l in body.splitlines() if l[:2].upper()=='VK']
areas = dict(a.split('=') for a in sys.argv[2:])
name = deck.rsplit('/',1)[-1][:-6]
dat = f'/home/user/c2/K/out/logs/{name}.dat'
c = ['.control', 'let k = 0', f'shell rm -f {dat}', 'while k < 133', '  let vx = k*0.05 - 3.3']
c += [f'  alter V{s} dc = $&vx' for s in srcs]
c += ['  ac lin 1 100k 100k']
c += ['* C per um2, fF/um2; I(V) flows into the + node, so C = -Im(I)/(2 pi f)']
c += [f'  let c{s.lower()} = -imag(i(v{s.lower()}))/(2*pi*100e3)/{areas[s]}e-12*1e3' for s in srcs]
c += ['  echo $&vx ' + ' '.join(f'$&c{s.lower()}' for s in srcs) + f' >> {dat}']
c += ['  destroy all', '  let k = k + 1', 'end', '.endc', '.end', '']
open(deck,'w').write(body + '\n'.join(c))
