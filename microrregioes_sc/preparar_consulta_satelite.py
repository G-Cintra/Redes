"""Cria uma consulta autocontida para colar no Code Editor do Earth Engine."""
import argparse
import json
from pathlib import Path

PASTA = Path(__file__).resolve().parent


def preparar(ano):
    if ano < 2019:
        raise ValueError("Use um ano completo a partir de 2019; TROPOMI não cobre a MIP de 2015.")
    malha = json.loads((PASTA / "dados/microrregioes_sc.geojson").read_text(encoding="utf-8"))
    codigo = "var regioes = ee.FeatureCollection(" + json.dumps(malha, ensure_ascii=False) + ");\n"
    codigo += f"var ano = {ano};\n"
    codigo += """
// Executar em https://code.earthengine.google.com/ com projeto habilitado.
var inicio = ee.Date.fromYMD(ano, 1, 1);
var fim = inicio.advance(1, 'year'); // limite exclusivo
var banda = 'tropospheric_NO2_column_number_density';
var colecao = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
  .filterDate(inicio, fim).filterBounds(regioes).select(banda);
print('Número de imagens; deve ser maior que zero', colecao.size());
// Média por dia evita dar peso extra a dias com órbitas sobrepostas.
var dias = ee.List.sequence(0, fim.difference(inicio, 'day').subtract(1));
var diario = ee.ImageCollection.fromImages(dias.map(function(d) {
  var data = inicio.advance(d, 'day');
  var imagens = colecao.filterDate(data, data.advance(1, 'day'));
  var vazio = ee.Image.constant(0).rename(banda).updateMask(ee.Image.constant(0));
  return ee.Image(ee.Algorithms.If(imagens.size().gt(0), imagens.mean(), vazio))
    .set('system:time_start', data.millis());
}));
var media = diario.mean().rename('no2_mol_m2');
var contagem = diario.count().unmask(0).rename('dias_validos');
// Média temporal por célula, depois média espacial ponderada por área válida.
var area = ee.Image.pixelArea();
var somas = media.multiply(area).rename('numerador')
  .addBands(area.updateMask(media.mask()).rename('area_valida_m2'))
  .addBands(contagem.multiply(area).rename('dias_area'))
  .addBands(area.rename('area_total_m2'))
  .reduceRegions({collection: regioes, reducer: ee.Reducer.sum(),
    crs: 'EPSG:4326', scale: 1113.2, tileScale: 4});
var tabela = somas.map(function(f) {
  var valida = ee.Number(f.get('area_valida_m2'));
  var total = ee.Number(f.get('area_total_m2'));
  return ee.Feature(null, {
    codigo_ibge: f.get('codigo_ibge'), microrregiao: f.get('microrregiao'),
    ano: ano, no2_mol_m2: ee.Algorithms.If(valida.gt(0),
      ee.Number(f.get('numerador')).divide(valida), null),
    fracao_area_observada: valida.divide(total),
    dias_validos_media_area: ee.Number(f.get('dias_area')).divide(total)
  });
});
print('Resultados e cobertura', tabela);
Map.centerObject(regioes, 7);
Map.addLayer(media.clipToCollection(regioes),
  {min: 0, max: 0.0001, palette: ['ffffcc', 'fd8d3c', '800026']}, 'Coluna NO2');
Export.table.toDrive({collection: tabela, description: 'SC_NO2_' + ano,
  fileFormat: 'CSV', selectors: ['codigo_ibge', 'microrregiao', 'ano',
    'no2_mol_m2', 'fracao_area_observada', 'dias_validos_media_area']});
// Preservar os IDs e versões usados na execução para auditoria.
var inventario = ee.FeatureCollection(colecao.toList(colecao.size()).map(function(i) {
  var imagem = ee.Image(i);
  return ee.Feature(null, imagem.toDictionary(['system:index', 'PRODUCT_ID',
    'PROCESSOR_VERSION', 'ALGORITHM_VERSION', 'system:time_start']));
}));
Export.table.toDrive({collection: inventario, description: 'SC_NO2_fontes_' + ano,
  fileFormat: 'CSV'});
"""
    destino = PASTA / "dados" / f"consulta_no2_{ano}.js"
    destino.write_text(codigo, encoding="utf-8")
    print(destino)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ano", type=int, required=True)
    preparar(parser.parse_args().ano)
